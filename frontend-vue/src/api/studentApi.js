import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export async function getGroups() {
    const response = await axios.get(`${API_URL}/groups`);
    return response.data;
}

export async function createGroup(group) {
    const response = await axios.post(
        `${API_URL}/groups`,
        group
    );

    return response.data;
}

export async function getStudents(search = "", groupId = null) {
    const response = await axios.get(`${API_URL}/students`, {
        params: {
            search: search || undefined,
            group_id: groupId ?? undefined
        }
    });

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

export async function deleteStudent(id) {
    await axios.delete(`${API_URL}/students/${id}`);
}

export async function getGroupStats() {
    const response = await axios.get(`${API_URL}/groups/stats`);
    return response.data;
}