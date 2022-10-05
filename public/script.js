$(document).ready(function(){

  // Load the initial table
  getEmployeeList();

  // Click event handler for the Add New Employee
  $("#addEmployee").on("click", function() {
    $("#addName").val("");
    $("#addEmail").val("");
    $("#addAddress").val("");
    $("#addPhone").val("");
  });

  // Save event handler for Add New Employee
  $("#addSave").on("click", function(e) {
    var empObj = {
      name: $("#addName").val(),
      email: $("#addEmail").val(),
      address: $("#addAddress").val(),
      phone: $("#addPhone").val()
    };
    addEmployee(empObj);
  });

  // Click event handler for Edit button
  $(document).on("click", ".edit", function() {
    var id = $(this).attr("dataid");
    $("#editSave").attr("dataid", id);
    editEmployee(id);
  });

  // Save event handler for saving edited changes.
  $("#editSave").on("click", function() {
    var id = $(this).attr("dataid");
    var empObj = {
      name: $("#editName").val(),
      email: $("#editEmail").val(),
      address: $("#editAddress").val(),
      phone: $("#editPhone").val()
    };
    updateEmployee(id, empObj);
  });

  // Click event handler for Delete button
  $(document).on("click", ".delete", function() {
    var id = $(this).attr("dataid");
    $("#deleteSave").attr("dataid", id);
  });

  // Save event handler for Delete button
  $("#deleteSave").on("click", function() {
    var id = $(this).attr("dataid");
    deleteEmployee(id);
  });
 
 
  // New Employee AJAX
  function addEmployee(empData) {
    $.ajax({
      url: "/api/employees",
      type: "POST",
      data: JSON.stringify(empData),
      contentType: "application/json",
      success: function(result) {
        $("#addCancel").click();
        getEmployeeList();
      },
      error: function(result) {
        if (result.status == 404) {
          alert("POST '/api/employees' endpoint not implemented or an error occurred.");
        }
        else
        {
          alert(result.responseText);
        }
      }
    });
  }

  // Update Employee AJAX
  function updateEmployee(empID, empData) {
    $.ajax({
      url: "/api/employees/" + empID,
      type: "PATCH",
      data: JSON.stringify(empData),
      contentType: "application/json",
      success: function(result) {
        $("#editCancel").click();
        getEmployeeList();
      },
      error: function(result) {
        if (result.status == 404) {
          alert("PATCH '/api/employees/:id' endpoint not implemented or an error occurred.");
        }
        else
        {
          alert(result.responseText);
        }
      }
    });
  }

  // Delete Employee AJAX
  function deleteEmployee(empID) {
    $.ajax({
      url: "/api/employees/" + empID,
      type: "DELETE",
      success: function(result) {
        $("#deleteCancel").click();
        getEmployeeList();
      },
      error: function(result) {
        if (result.status == 404) {
          alert("DELETE '/api/employees/:id' endpoint not implemented or an error occurred.");
        }
        else
        {
          alert(result.responseText);
        }
      }
    });
  }

  // List Employee AJAX
  function getEmployeeList() {
    var html = "";

    $.ajax({
      url: "/api/employees",
      type: "GET",
      success: function(result) {
        $("#tableBody").empty();
        
        for(var i = 0; i < result.length; i++) {
          
          html +=
            `<tr>
                <td>
                  <span class="custom-checkbox">
                    <input type="checkbox" value="1">
                    <label for="checkbox1"></label>
                  </span>
                </td>
                <td>${result[i].name}</td>
                <td><a href="mailto:${result[i].email}">${result[i].email}</a></td>
                <td>${result[i].address}</td>
                <td>${result[i].phone}</td>
                <td>
                    <a href="#editEmployeeModal" dataid="${result[i].id}" class="edit" data-toggle="modal"><i class="material-icons" data-toggle="tooltip" title="Edit">&#xE254;</i></a>
                    <a href="#deleteEmployeeModal" dataid="${result[i].id}" class="delete" data-toggle="modal"><i class="material-icons" data-toggle="tooltip" title="Delete">&#xE872;</i></a>
                </td>
            </tr>`;
        }
        $("#tableBody").append(html);
      },
      error: function(result) {
        if (result.status == 404) {
          alert("GET '/api/employees' endpoint not implemented or an error occurred.");
        }
        else
        {
          alert(result.responseText);
        }
      }
    });
  }

  // Edit Employee AJAX
  function editEmployee(empID) {
    $.ajax({
      url: "/api/employees/" + empID,
      type: "GET",
      success: function(result) {
        if (result) {
          $("#editName").val(result.name);
          $("#editEmail").val(result.email);
          $("#editAddress").val(result.address);
          $("#editPhone").val(result.phone);
        }
      },
      error: function(result) {
        if (result.status == 404) {
          alert("GET '/api/employees/:id' endpoint not implemented or an error occurred.");
        }
        else
        {
          alert(result.responseText);
        }
      }
    });
  }

	// Activate tooltip
	$('[data-toggle="tooltip"]').tooltip();
	
	// Select/Deselect checkboxes
	var checkbox = $('table tbody input[type="checkbox"]');
	$("#selectAll").click(function(){
		if(this.checked){
			checkbox.each(function(){
				this.checked = true;                        
			});
		} else{
			checkbox.each(function(){
				this.checked = false;                        
			});
		} 
	});
	checkbox.click(function(){
		if(!this.checked){
			$("#selectAll").prop("checked", false);
		}
	});
});