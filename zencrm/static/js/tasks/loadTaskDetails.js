function loadTaskDetails(taskId) {	
    $.ajax({
        url: '/tasks/detail/' + taskId,  
        type: 'GET',
        dataType: 'json',
        success: function(task) {                        
            $('.task-id').each(function() {
                if (task.id != null && task.id != "") {
                    $(this).html(task.id); 
                } else {
                    $(this).html("None"); 
                }
            });
            $('.task-name').each(function() {
                if (task.name != null && task.name != "") {
                    $(this).html(task.name); 
                } else {
                    $(this).html("None"); 
                }
            });

            $('.task-assigned-to').each(function() {                                    
                if (task.assigned_to != null && task.assigned_to != "") {
                    $(this).html(task.assigned_to); 
                } else {
                    $(this).html("None"); 
                }
            });

            $('.task-category').each(function() {                    
                if (task.category != null && task.category != "") {
                    $(this).html(task.category); 
                } else {
                    $(this).html("None"); 
                }
            });

            $('.task-due-date').each(function() {                                    
                if (task.due_date != null && task.due_date != "") {
                    $(this).html(task.due_date); 
                } else {
                    $(this).html("None"); 
                }
            });

            $('.task-start-date').each(function() {                    
                if (task.start_date != null && task.start_date != "") {
                    $(this).html(task.start_date); 
                } else {
                    $(this).html("None"); 
                }
            });

            $('.task-reminder-date').each(function() {                    
                if (task.reminder_date != null && task.reminder_date != "") {
                    $(this).html(task.reminder_date); 
                } else {
                    $(this).html("None"); 
                }
            });

            $('.task-progress').each(function() {                    
                if (task.progress != null && task.progress != "") {
                    $(this).html(task.progress); 
                } else {
                    $(this).html("None"); 
                }
            });
                        
            $('.task-priority').each(function() {                                    
                if (task.priority != null && task.priority != "") {
                    $(this).html(task.priority); 
                } else {
                    $(this).html("None"); 
                }
            });

            $('.task-status').each(function() {                    
                if (task.status != null && task.status != "") {
                    $(this).html(task.status); 
                } else {
                    $(this).html("None"); 
                }
            });
                
            $('.task-related-to').each(function() {                    
                if (task.related_to != null && task.related_to != "") {
                    $(this).html(task.related_to); 
                } else {
                    $(this).html("None"); 
                }
            });

            $('.task-description').each(function() {                    
                if (task.description != null && task.description != "") {
                    $(this).html(task.description); 
                } else {
                    $(this).html("None"); 
                }
            });

            $('.task-created-by').each(function() {                    
                if (task.created_by != null && task.created_by != "") {
                    $(this).html(task.created_by); 
                } else {
                    $(this).html("None"); 
                }
            });

            $('.task-owner').each(function() {                    
                if (task.record_owner != null && task.record_owner != "") {
                    $(this).html(task.record_owner); 
                } else {
                    $(this).html("None"); 
                }
            });

            $('.task-visibility').each(function() {                    
                if (task.task_visibility != null && task.task_visibility != "") {
                    $(this).html(task.task_visibility); 
                } else {
                    $(this).html("None"); 
                }
            });

            $('.task-created-at').each(function() {                    
                if (task.created != null && task.created != "") {
                    $(this).html(task.created); 
                } else {
                    $(this).html("None"); 
                }
            });
            
            $('.task-updated-at').each(function() {                    
                if (task.updated != null && task.updated != "") {
                    $(this).html(task.updated); 
                } else {
                    $(this).html("None"); 
                }
            });            
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
}