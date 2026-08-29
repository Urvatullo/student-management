import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export async function getStudents() {
    const response = await axios.get(`${API_URL}/students`);
    return response.data;
}

export async function createStudent(student) {
    const response = await axios.post(
        `${API_URL}/students`,
        student
    );

    return response.data;
}

export async function updateStudent(id, student) {
    const response = await axios.put(
        `${API_URL}/students/${id}`,
        student
    );

    return response.data;
}

export async function deleteStudent(id, student) {
    await axios.delete(`${API_URL}/students/${id}`);
}