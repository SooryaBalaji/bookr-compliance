import http from 'k6/http';
import { check, sleep } from 'k6';

// 1. The Stress Profile: Ramp up, hold peak, ramp down
export const options = {
  stages: [
    { duration: '5s', target: 15 },  // Ramp up to 15 concurrent users
    { duration: '15s', target: 30 }, // Peak stress at 30 users constantly hammering CRUD
    { duration: '5s', target: 0 },   // Ramp down to 0
  ],
};

const baseURL = 'http://web:8000';

// Auth + the Task schema changed since this script was written:
//   - Every mutating endpoint now requires the httponly `bookr_token` cookie
//     set by /auth/register or /auth/login (there is no bearer token).
//   - Task creation now requires a valid `entity_id` (400 if missing), and
//     TaskCreate has no `description`/`status` fields (it uses short/title/
//     due_type/... instead); TaskUpdate (the PATCH body) only accepts
//     due_type/due_month/due_day/due_text.
//
// setup() runs once (not per-VU): it bootstraps a super_admin account via
// /auth/register (works only for the very first user in a fresh DB), grabs
// the auth cookie from the Set-Cookie response, and creates one throwaway
// Entity to hang test Tasks off of. The cookie + entity id are then handed
// to every VU via the setup->default `data` argument.
export function setup() {
  const uniq = `${Date.now()}_${Math.floor(Math.random() * 1e6)}`;

  const registerRes = http.post(
    `${baseURL}/auth/register`,
    JSON.stringify({
      email: `loadtest_${uniq}@example.com`,
      password: 'LoadTest123!',
      full_name: 'K6 Load Test',
    }),
    { headers: { 'Content-Type': 'application/json' } }
  );

  if (registerRes.status !== 200 || !registerRes.cookies['bookr_token']) {
    throw new Error(
      `setup(): /auth/register failed (status ${registerRes.status}): ${registerRes.body}`
    );
  }
  const cookie = registerRes.cookies['bookr_token'][0].value;
  const authHeaders = {
    'Content-Type': 'application/json',
    Cookie: `bookr_token=${cookie}`,
  };

  const entityRes = http.post(
    `${baseURL}/entities/`,
    JSON.stringify({
      name: `Load Test Entity ${uniq}`,
      org_type: 'LLC',
      incorporation_state: 'Delaware',
      headquarters: 'Wilmington, DE',
      naics_code: '541511',
      creation_template: 'custom',
      is_restricted: false,
    }),
    { headers: authHeaders }
  );

  if (entityRes.status !== 200) {
    throw new Error(
      `setup(): /entities/ failed (status ${entityRes.status}): ${entityRes.body}`
    );
  }
  const entityId = entityRes.json().id;

  return { cookie, entityId };
}

export default function (data) {
  const headers = {
    'Content-Type': 'application/json',
    Cookie: `bookr_token=${data.cookie}`,
  };

  // Create
  const postPayload = JSON.stringify({
    short: 'Load Test Task',
    title: 'Performance Test Task',
    entity_id: data.entityId,
  });

  const postRes = http.post(`${baseURL}/tasks/`, postPayload, { headers });
  const postSuccess = check(postRes, {
    'POST success (200)': (r) => r.status === 200,
  });

  // Only proceed if the task was successfully created
  if (postSuccess) {
    const task = postRes.json();
    const taskId = task.id;

    // Read
    const getRes = http.get(`${baseURL}/tasks/`, { headers });
    check(getRes, {
      'GET success (200)': (r) => r.status === 200,
    });

    // Update (this is a PATCH, not a PUT; TaskUpdate only takes due_* fields)
    const patchPayload = JSON.stringify({
      due_type: 'fixed',
      due_month: 6,
      due_day: 15,
      due_text: 'Updated via load test',
    });

    const patchRes = http.patch(`${baseURL}/tasks/${taskId}`, patchPayload, { headers });
    check(patchRes, {
      'PATCH success (200)': (r) => r.status === 200,
    });

    // Delete
    const delRes = http.del(`${baseURL}/tasks/${taskId}`, null, { headers });
    check(delRes, {
      'DELETE success (200)': (r) => r.status === 200,
    });
  }

  // A tiny 100ms pause to let the database connections cycle
  sleep(0.1);
}