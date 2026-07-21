const { test, expect } = require('@playwright/test');

// Because Playwright is running inside the Docker network,
// it talks directly to the backend container named 'web'.
const baseURL = process.env.API_BASE_URL || 'http://web:8000';

// The API now requires an authenticated, cookie-based session for every
// mutating endpoint (see app/main.py: get_current_editor / get_current_user).
// Only the FIRST user ever registered becomes super_admin; after that,
// public registration is disabled (403). So this suite either bootstraps
// the very first admin on a fresh database, or logs in with credentials
// supplied via TEST_ADMIN_EMAIL / TEST_ADMIN_PASSWORD env vars.
const TEST_ADMIN_EMAIL = process.env.TEST_ADMIN_EMAIL || `qa+${Date.now()}@bookr.test`;
const TEST_ADMIN_PASSWORD = process.env.TEST_ADMIN_PASSWORD || 'TestPass123!';

test.describe('Bookr Compliance API - Task CRUD Lifecycle', () => {
  let apiContext;   // Shared context so the auth cookie persists across tests
  let taskId;
  let entityId;

  test.beforeAll(async ({ playwright }) => {
    apiContext = await playwright.request.newContext({ baseURL });

    const initRes = await apiContext.get('/auth/is-initialized');
    const { initialized } = await initRes.json();

    if (!initialized) {
      // Fresh database: register the first user, which becomes super_admin
      // and sets the auth cookie on this context automatically.
      const registerRes = await apiContext.post('/auth/register', {
        data: { email: TEST_ADMIN_EMAIL, password: TEST_ADMIN_PASSWORD, full_name: 'QA Bot' },
      });
      expect(registerRes.ok()).toBeTruthy();
    } else {
      // Already initialized: log in with pre-provisioned test credentials.
      // TEST_ADMIN_EMAIL / TEST_ADMIN_PASSWORD must be set in CI for this path.
      const loginRes = await apiContext.post('/auth/login', {
        form: { username: TEST_ADMIN_EMAIL, password: TEST_ADMIN_PASSWORD },
      });
      expect(loginRes.ok(), 'Login failed — set TEST_ADMIN_EMAIL/TEST_ADMIN_PASSWORD for an existing account').toBeTruthy();
    }

    // Tasks require a target entity; grab the first available one, or skip
    // entity-scoping if none exist (super_admin can still create org-less tasks).
    const entitiesRes = await apiContext.get('/entities/');
    if (entitiesRes.ok()) {
      const entities = await entitiesRes.json();
      if (entities.length > 0) entityId = entities[0].id;
    }
  });

  test.afterAll(async () => {
    await apiContext.dispose();
  });

  test('1. POST /tasks/ - Create a task', async () => {
    const response = await apiContext.post('/tasks/', {
      data: {
        short: 'QA-TEST',
        title: 'Automated Robot Audit',
        scope: 'Internal',
        quarter: 'ROLL',
        due_type: 'rolling',
        due_text: 'Rolling Milestone',
        entity_id: entityId,
        info: 'Created by the automated API test suite.',
      },
    });

    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data.title).toBe('Automated Robot Audit');
    taskId = data.id;
  });

  test('2. GET /tasks/ - List tasks', async () => {
    const response = await apiContext.get('/tasks/');
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(Array.isArray(data)).toBeTruthy();
    expect(data.some(t => t.id === taskId)).toBeTruthy();
  });

  test('3. PATCH /tasks/{task_id} - Update the due date', async () => {
    const response = await apiContext.patch(`/tasks/${taskId}`, {
      data: {
        due_type: 'fixed',
        due_month: 6,
        due_day: 15,
        due_text: 'June 15',
      },
    });
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data.status).toBe('success');
  });

  test('4. PATCH /tasks/{task_id} - Rejects unauthenticated requests', async ({ playwright }) => {
    // Regression test for the previously-missing auth check on this route.
    const anonContext = await playwright.request.newContext({ baseURL });
    const response = await anonContext.patch(`/tasks/${taskId}`, {
      data: { due_type: 'fixed', due_month: 1, due_day: 1, due_text: 'January 1' },
    });
    expect(response.status()).toBe(401);
    await anonContext.dispose();
  });

  test('5. DELETE /tasks/{task_id} - Soft-delete the task', async () => {
    const response = await apiContext.delete(`/tasks/${taskId}`);
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data.status).toBe('success');
  });
});