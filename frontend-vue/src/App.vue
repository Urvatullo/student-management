<script setup>
  import { computed, ref } from "vue";
import StudentCard from "./components/StudentCard.vue";

  const editingIndex = ref(null);

  const students = ref([
      {
        name: "Urvatullo",
        age: 21,
        group: "IT-101"
      },
      {
        name: "Qosim",
        age: 27,
        group: "IT-102"
      },
      {
        name: "Muhammad",
        age: 25,
        group: "IT-103"
      }
  ]);

  const name = ref("");
  const age = ref("");
  const group = ref("");

  function addStudent() {
    if(editingIndex.value !== null) {
      students.value[editingIndex.value] = {
        name: name.value,
        age: Number(age.value),
        group: group.value
      };

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
   
    students.value.push(newStudent);
    console.log(newStudent);

    name.value = "";
    age.value = "";
    group.value = "";
  }

  function editStudent(student) {
    editingIndex.value = students.value.indexOf(student);

    name.value = students.name;
    age.value = students.age;
    group.value = students.group;

  }

  function deleteStudent(student) {
    const index = students.value.indexOf(student);

    students.value.splice(index,1);
  }

  const search = ref("");

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
      v-for="(student, index) in filteredStudents" 
      :key="student.name"
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
