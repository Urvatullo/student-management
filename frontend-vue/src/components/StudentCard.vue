<script setup>
import { ref } from "vue";

const confirmDelete = ref(false);

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
        <button
            v-if="!confirmDelete"
            class="delete-button"
            @click="confirmDelete = true"
        >
            Delete
        </button>

        <div v-else class="delete-confirm">
            <span>Are you sure?</span>

            <button
                class="cancel-delete"
                @click="confirmDelete = false"
            >
                Cancel
            </button>

            <button
                class="confirm-delete"
                @click="$emit('delete'); confirmDelete = false"
            >
                Delete
            </button>
        </div>
    </div>
</template>

<style scoped>
.delete-button {
    background-color: #dc2626;
    color: white;
}

.delete-button:hover {
    background-color: #b91c1c;
}

.delete-confirm {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}

.delete-confirm span {
    width: 100%;
    color: #b91c1c;
    font-weight: 600;
    margin-bottom: 5px;
}

.cancel-delete {
    background-color: #6b7280;
    color: white;
}

.cancel-delete:hover {
    background-color: #4b5563;
}

.confirm-delete {
    background-color: #dc2626;
    color: white;
}

.confirm-delete:hover {
    background-color: #b91c1c;
}

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
