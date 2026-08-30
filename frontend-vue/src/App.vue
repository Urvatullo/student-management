<script setup>
import { onMounted, ref } from "vue";
import {
    getStudents,
    createStudent,
    updateStudent,
    deleteStudent as deleteStudentApi,
    getGroups,
    createGroup,
    getGroupStats
} from "./api/studentApi";

import StudentCard from "./components/StudentCard.vue";

  const editingIndex = ref(null);

  const students = ref([]);

  const groups = ref([]);

  const groupStats = ref([]);

  const errorMessage = ref("");
  const successMessage = ref("");
  const newGroupName = ref("");
  const name = ref("");
  const age = ref("");
  const group = ref("");

  async function loadStudents() {
      students.value = await getStudents(
          search.value,
          selectedGroup.value
      );
  }

  async function addStudent() {
      errorMessage.value = "";
      successMessage.value = "";

      if (name.value.trim() === "" || age.value === "" || group.value === "") {
          errorMessage.value = "Please fill in all fields";
          return;
      }

      try {
          if (editingIndex.value !== null) {
              const id = students.value[editingIndex.value].id;

              const updatedStudent = {
                  name: name.value,
                  age: Number(age.value),
                  group_id: Number(group.value)
              };

              const result = await updateStudent(id, updatedStudent);

              students.value[editingIndex.value] = result;

              editingIndex.value = null;

              name.value = "";
              age.value = "";
              group.value = "";

              successMessage.value = "Student updated successfully!";
              return;
          }

          const newStudent = {
              name: name.value,
              age: Number(age.value),
              group_id: Number(group.value)
          };

          const createdStudent = await createStudent(newStudent);

          students.value.push(createdStudent);

          name.value = "";
          age.value = "";
          group.value = "";

          successMessage.value = "Student added successfully!";
      } catch (error) {
          errorMessage.value =
              error.response?.data?.detail || "Failed to save student";
      }
  }

  function editStudent(student) {
      editingIndex.value = students.value.indexOf(student);

      name.value = student.name;
      age.value = student.age;
      group.value = String(student.group_id);
  }

  async function deleteStudent(student) {
      errorMessage.value = "";
      successMessage.value = "";

      try {
          await deleteStudentApi(student.id);

          students.value = students.value.filter(
              s => s.id !== student.id
          );

          successMessage.value = "Student deleted successfully!";
      } catch (error) {
          errorMessage.value =
              error.response?.data?.detail || "Failed to delete student";
      }
  }

  const search = ref("");

  const selectedGroup = ref(null);

  onMounted(async () => {
    const [loadedGroups, loadedGroupStats] = await Promise.all([
      getGroups(),
      getGroupStats()
  ]);

  groups.value = loadedGroups;
  groupStats.value = loadedGroupStats;

  await loadStudents();
  });

</script>

/////////////////////////////////////////////////////////////////

<template>
  <h1>Student Management System</h1>

  <div v-if="errorMessage" class="message error-message">
      {{ errorMessage }}
  </div>

  <div v-if="successMessage" class="message success-message">
      {{ successMessage }}
  </div>

  <div class="groups-section">
      <h2>Groups</h2>

      <div class="groups-grid">
          <div
              v-for="item in groupStats"
              :key="item.id"
              class="group-card"
              @click="selectedGroup = item.id; loadStudents()"
          >
              <h3>{{ item.name }}</h3>

              <p>
                  Students:
                  <strong>{{ item.student_count }}</strong>
              </p>
          </div>
      </div>
  </div>

  <div class="add-group-form">
      <h2>Add Group</h2>

      <input
          v-model="newGroupName"
          placeholder="Group name"
      >

      <button
          class="add-button"
          @click="addGroup"
      >
          Add Group
      </button>
  </div>

  <div class="add-student-form">
    <h2>Add Student</h2>

    <input v-model="name" placeholder="Name">

    <input v-model="age" type="number" placeholder="Age">

    <select v-model="group">
      <option disabled value="">Choose a group</option>

      <option
        v-for="item in groups"
        :key="item.id"
        :value="item.id"
      >
        {{ item.name }}
      </option>
    </select>

    <button class="add-button" @click="addStudent">{{ editingIndex === null ? "Add Student" : "Edit Student" }}</button>
  </div>

  <div class="search-box">
      <input
          v-model="search"
          class="search-input"
          placeholder="Search student..."
          @keyup.enter="loadStudents"
      >

      <button
          class="search-button"
          @click="loadStudents"
      >
          Search
      </button>
  </div>

  <div v-if="selectedGroup !== null" class="filter-info">
      Showing:
      <strong>
          {{ groupStats.find(g => g.id === selectedGroup)?.name }}
      </strong>

      <button @click="selectedGroup = null; loadStudents()">
          Show All
      </button>
  </div>

  <h2>Students</h2>

  <div class="students-grid">
    <StudentCard
        v-for="student in students"
        :key="student.id"
        :student="student"
        @delete="deleteStudent(student)"
        @edit="editStudent(student)"
    />
</div>
</template>

////////////////////////////////////////////////////////////////

<style scoped>
.message {
    max-width: 500px;
    margin: 15px auto;
    padding: 12px 16px;
    border-radius: 8px;
    text-align: center;
    font-weight: 600;
}

.error-message {
    background-color: #fee2e2;
    color: #b91c1c;
    border: 1px solid #fecaca;
}

.success-message {
    background-color: #dcfce7;
    color: #15803d;
    border: 1px solid #bbf7d0;
}

.group-card {
    cursor: pointer;
    transition: 0.2s;
}

.group-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.filter-info {
    max-width: 900px;
    margin: 20px auto;
    padding: 12px 16px;
    background: #eef4ff;
    border-radius: 8px;
    text-align: center;
}

.filter-info button {
    margin-left: 15px;
    background: #6b7280;
    color: white;
}

.filter-info button:hover {
    background: #4b5563;
}

.groups-section {
    max-width: 900px;
    margin: 30px auto;
}

.groups-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.group-card {
    padding: 20px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    text-align: center;
}

.group-card h3 {
    margin-top: 0;
    color: darkblue;
}

.group-card p {
    margin-bottom: 0;
    color: #555;
}

.group-card strong {
    color: #2563eb;
}

.add-student-form select {
  display: block;
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  background-color: white;
  cursor: pointer;
}

.add-student-form select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.add-group-form {
  max-width: 500px;
  margin: 20px auto;
  padding: 25px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.add-group-form h2 {
  margin-top: 0;
  margin-bottom: 18px;
  color: darkblue;
  text-align: center;
}

.add-group-form input {
  display: block;
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
}

.add-group-form input:focus {
  outline: none;
  border-color: #16a34a;
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.15);
}

.add-group-form .add-button {
  width: 100%;
  padding: 11px;
  border: none;
  border-radius: 6px;
  background-color: #16a34a;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.add-group-form .add-button:hover {
  background-color: #15803d;
}

.add-group-form .add-button:active {
  transform: scale(0.97);
}

.search-box {
    display: flex;
    gap: 10px;
    max-width: 500px;
    margin: 20px auto;
}

.search-input {
    flex: 1;
    box-sizing: border-box;
    padding: 11px 14px;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 16px;
}

.search-input:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.search-button {
    padding: 11px 20px;
    border: none;
    border-radius: 6px;
    background-color: #2563eb;
    color: white;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: 0.2s;
}

.search-button:hover {
    background-color: #1d4ed8;
}

.search-button:active {
    transform: scale(0.97);
}

button {
  padding: 10px 18px;
  border: none;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

h1{
  margin-top: 0;
  color: darkblue;
  text-align: center;
}

h2 {
  margin-top: 0;
  color: darkblue;
  text-align: center;
}

.add-button {
  width: 100%;
  background-color: #2563eb;
  color: white;
}

.add-button:hover {
  background-color: #1d4ed8;
}

button:active {
  transform: scale(0.97);
}

.students-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.add-student-form {
  max-width: 500px;
  margin: 20px auto;
  padding: 25px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.add-student-form h2 {
  margin-top: 0;
  color: darkblue;
}

.add-student-form input {
  display: block;
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
}

.add-student-form button {
  width: 100%;
  padding: 11px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
}

</style>
