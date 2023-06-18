var tasks = []; // Array to store the tasks


// this is for generating with ai
function generate() {
    fetch('/generate', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({tasks: tasks})
    })
    .then(response => response.text())
    .then(result => {
        console.log(result);
    })
    .catch(error => {
        console.error('Error:', error);
    });

    var table = document.getElementById("todo-list");
    // sortTableByPriority(table)
    for(let i = 0; i < result.length; i++){
        var row = table.insertRow(i);
        row.insertCell(0).innerHTML = result[i][0];
        row.insertCell(1).innerHTML = result[i][1];
        row.insertCell(2).innerHTML = result[i][2];
    }
    
}

// function sortTableByPriority(table) {
//     var rows = Array.from(table.rows)
    

//     while (table.rows.length > 1) {
//         table.deleteRow(1);
//     }

//     rows = rows.slice(1);

//     rows.sort(function (rowA, rowB) {
//         var priorityA = getPriorityValue(rowA.cells[2].innerHTML);
//         var priorityB = getPriorityValue(rowB.cells[2].innerHTML);
//         return priorityB - priorityA; // Sorting in descending order
//     });

//     // Re-insert sorted rows into the table
//     for (var i = 0; i < rows.length; i++) {
//         table.appendChild(rows[i]);
//     }
// }

// function getPriorityValue(priority) {
//     switch (priority.toLowerCase()) {
//         case "Highest":
//         return 4;
//         case "High":
//         return 3;
//         case "Medium":
//         return 2;
//         case "Low":
//         return 1;
//         case "Lowest":
//         return 0;
//         default:
//         return -1; // Invalid priority value
//     }
// }  
// dont change this is for adding tasks
document.getElementById("todo-form").addEventListener("submit", function(event) {
    event.preventDefault();
        
    var name = document.getElementById("todo-input-name");
    var loc = document.getElementById("autocomplete");
    var dur = document.getElementById("todo-input-dur");
    if (dur == 0) { dur = 30; }
    var pri = document.getElementById("todo-input-pri");
    var todoItem = document.createElement("li");
    var table = document.getElementById("todo-list");
    todoItem.textContent = name.value + " " + dur.value + " minutes " + pri.value + " priority";

    // appending old tasks
    tasks = [...tasks, [name.value, loc.value, dur.value, pri.value]];
    //document.getElementById("todo-list-raw").appendChild(todoItem);

    console.log(name.value, loc.value, dur.value, pri.value)

    var rowCount = table.rows.length;
    var row = table.insertRow(rowCount);
    row.insertCell(0).innerHTML = name.value;
    row.insertCell(1).innerHTML = loc.value;
    row.insertCell(2).innerHTML = dur.value;
    row.insertCell(3).innerHTML = pri.value;
    //sortTableByPriority(table)

    // reset input fields
    name.value = "";
    loc.value = "";
    dur.value = "";
    pri.value = "";


}); 
