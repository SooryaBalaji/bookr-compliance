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

export default function () {
  const headers = { 'Content-Type': 'application/json' };

  // Create
  const postPayload = JSON.stringify({
    title: "Performance Test Task",
    description: "Stress testing database writes under pressure",
    status: "Pending"
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
    const getRes = http.get(`${baseURL}/tasks/`);
    check(getRes, {
      'GET success (200)': (r) => r.status === 200,
    });

    // Update
    const putPayload = JSON.stringify({
      title: "Performance Test Task - Updated",
      description: "Stress testing database writes under pressure",
      status: "Complete"
    });

    const putRes = http.put(`${baseURL}/tasks/${taskId}`, putPayload, { headers });
    check(putRes, {
      'PUT success (200)': (r) => r.status === 200,
    });

    // Delete
    const delRes = http.del(`${baseURL}/tasks/${taskId}`);
    check(delRes, {
      'DELETE success (200)': (r) => r.status === 200,
    });
  }

  // A tiny 100ms pause to let the database connections cycle
  sleep(0.1);
}