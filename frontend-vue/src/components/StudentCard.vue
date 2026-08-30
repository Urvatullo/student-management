<script setup>
const props = defineProps ({
    student: Object
});

const emit = defineEmits(["delete", "edit"]);

</script>

<template>
    <div class="student-card">
        <h3>{{ props.student.name }}</h3>
        <p>Age: {{ props.student.age }}</p>
        <p>Group: {{ props.student.group.name }}</p>

        <button class="edit-button" @click="emit('edit')">
            Edit
        </button>
        <button class="delete-button" @click="emit('delete')">
            Delete
        </button>
    </div>
</template>

<style scoped>
button {
  padding: 10px 18px;
  border: none;
  border-radius: 0;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.delete-button {
  background-color: #ef4444;
  color: white;
}

.delete-button:hover {
  background-color: #dc2626;
}

.edit-button {
  background-color: #f59e0b;
  color: white;
  margin-right: 8px;
}

.edit-button:hover {
  background-color: #d97706;
}

.student-card {
  background-color: white;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.student-card h3 {
  margin-top: 0;
  color: darkblue;
}

.student-card p {
  margin: 8px 0;
}

.student-card button {
  margin-top: 15px;
  padding: 8px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  width: calc(50% - 4px);
}
</style>
