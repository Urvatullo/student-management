<script setup>
import { computed, onMounted, ref } from "vue";
import {
   getStudents, 
   createStudent, 
   updateStudent, 
   deleteStudent as deleteStudentApi 
  } from "./api/studentApi";

import StudentCard from "./components/StudentCard.vue";

  const editingIndex = ref(null);

  const students = ref([]);

  const name = ref("");
  const age = ref("");
  const group = ref("");

  async function addStudent() {
    if (editingIndex.value !== null) {
        const id = students.value[editingIndex.value].id;

        const updatedStudent = {
            name: name.value,
            age: Number(age.value),
            group: group.value
        };

        const result = await updateStudent(id, updatedStudent);

        students.value[editingIndex.value] = result;

        editingIndex.value = null;

        name.value = "";
        age.value = "";
        group.value = "";

        return;
    }

    if(name.value === "" || age.value === "" || group.value === "") {
      console.log("Please fill in all fields");
      return;
    }

    const newStudent = {
        name: name.value,
        age: Number(age.value),
        group: group.value
    };

    const createdStudent = await createStudent(newStudent);

    students.value.push(createdStudent);

    console.log(createdStudent);

    name.value = "";
    age.value = "";
    group.value = "";
  }

  function editStudent(student) {
      editingIndex.value = students.value.indexOf(student);

      name.value = student.name;
      age.value = student.age;
      group.value = student.group;
  }

  async function deleteStudent(student) {
      await deleteStudentApi(student.id);

      students.value = students.value.filter(
          s => s.id !== student.id
      );
  }

  const search = ref("");

  onMounted(async () => {
      students.value = await getStudents();
  });

  const filteredStudents = computed(() => {
    return students.value.filter(student =>
      student.name.toLowerCase().includes(search.value.toLowerCase())
    );
  })

</script>

/////////////////////////////////////////////////////////////////

<template>
  <h1>Student Management System</h1>

  <div class="add-student-form">
    <h2>Add Student</h2>

    <input v-model="name" placeholder="Name">

    <input v-model="age" type="number" placeholder="Age">

    <input v-model="group" placeholder="Group">

    <button class="add-button" @click="addStudent">{{ editingIndex === null ? "Add Student" : "Edit Student" }}</button>
  </div>

  <input
    v-model="search"
    class="search-input"
    placeholder="Search student..."
  >

  <h2>Students</h2>

  <div class="students-grid">
    <StudentCard
        v-for="(student in filteredStudents"
        :key="student.id"
        :student="student"
        @delete="deleteStudent(student)"
        @edit="editStudent(student)"
    />
</div>
</template>

////////////////////////////////////////////////////////////////

<style scoped>

.search-input {
  display: block;
  width: min(500px, 100%);
  box-sizing: border-box;
  margin: 20px auto;
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

button {
  padding: 10px 18px;
  border: none;
  border-radius: none;
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
