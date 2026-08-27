const systemName = "Student Management System"

let studentsNumber = 3;

const students0 = [
    {
        name: "Urvatullo",
        age: 21,
        group: "IT - 101"
    },    
    {
        name: "Qosim",
        age: 27,
        group: "IT - 102"
    },
    {
        name: "Muhammad",
        age: 25,
        group: "IT - 103"
    },
];

////////////////////////////////////////////////////////////////////////////

const title = document.getElementById("title");
title.textContent = "Student Management System";

const button = document.getElementById("changeButton")

button.addEventListener("click",function(){
    title.textContent = "Hello From JavaScript";
});

const button1 = document.getElementById("showStudentsButton")

button1.addEventListener("click", function(){
    title.textContent = "Students List";
})

const nameInput = document.getElementById("nameInput");
const ageInput = document.getElementById("ageInput");
const groupInput = document.getElementById("groupInput");

const addStudentButton = document.getElementById("addStudentButton");

/********************************************************************/
const studentsList = document.getElementById("studentsList");

studentsList.classList.add("students");

function displayStudents() {
    studentsList.innerHTML = "";

    students0.forEach(function(student, index){
        const studentCard = document.createElement("div");
        studentCard.classList.add("student");

        const studentName = document.createElement("h3");
        studentName.textContent = student.name;

        const studentAge = document.createElement("p");
        studentAge.textContent = `Age: ${student.age}`;

        const studentGroup = document.createElement("p");
        studentGroup.textContent = `Group: ${student.group}`;

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", function(){
            students0.splice(index, 1);
            displayStudents();
        });

        studentCard.appendChild(studentName);
        studentCard.appendChild(studentAge);
        studentCard.appendChild(studentGroup);
        studentCard.appendChild(deleteButton);

        studentsList.appendChild(studentCard);
    });
}

displayStudents();

addStudentButton.addEventListener("click", function(){

    if (
        nameInput.value === "" ||
        ageInput.value === "" ||
        groupInput.value === ""
    ) {
        console.log("Please fill in all fields");
        return;
    }

    const newStudent = {
        name: nameInput.value,
        age: Number(ageInput.value),
        group: groupInput.value
    };

    students0.push(newStudent);

    nameInput.value = "";
    ageInput.value = "";
    groupInput.value = "";

    displayStudents();
});