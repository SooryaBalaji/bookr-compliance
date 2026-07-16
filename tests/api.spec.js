const { test, expect } = require('@playwright/test');

// Because Playwright is running inside the Docker network,
// it talks directly to the backend container named 'web'.
const baseURL = 'http://web:8000';

test.describe('Bookr Compliance API - Vault CRUD Lifecycle', () => {
  let taskId; // Variable to remember the ID of the task we create

  test('1. POST /tasks/ - Create a task', async ({ request }) => {
    const response = await request.post(`${baseURL}/tasks/`, {
      data: {
        title: "Automated Robot Audit",
        description: "Checking vault integrity",
        status: "Pending"
      }
    });

    // Assert the server returned a 200 OK
    expect(response.ok()).toBeTruthy();

    // Assert the data matches what we sent
    const data = await response.json();
    expect(data.title).toBe("Automated Robot Audit");

    // Save the ID so the next tests know which task to modify
    taskId = data.id;
  });

  test('2. GET /tasks/ - Read the vault', async ({ request }) => {
    const response = await request.get(`${baseURL}/tasks/`);
    expect(response.ok()).toBeTruthy();

    const data = await response.json();
    expect(Array.isArray(data)).toBeTruthy();
  });

  test('3. PUT /tasks/{task_id} - Update the task', async ({ request }) => {
    const response = await request.put(`${baseURL}/tasks/${taskId}`, {
      data: {
        title: "Automated Robot Audit",
        description: "Checking vault integrity",
        status: "Complete" // Changing the status
      }
    });
    expect(response.ok()).toBeTruthy();

    const data = await response.json();
    expect(data.status).toBe("Complete");
  });

  test('4. DELETE /tasks/{task_id} - Destroy the task', async ({ request }) => {
    const response = await request.delete(`${baseURL}/tasks/${taskId}`);
    expect(response.ok()).toBeTruthy();

    const data = await response.json();
    expect(data.status).toBe("success");
  });
});