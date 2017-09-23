$( document ).ready(function() {
		$("#login-button").click(function(){
				login();
		});


	});

function login()
{
		please_wait();
		var username = $("#username-input").val();
		var passwd = $("#password-input").val();

		var request = {};
		request["username"] = username;
		request["password"] = passwd;
		
		if(validate_passwd(passwd))
		{
			$.post(
				"http://localhost/textReader/" + "login.py/login",
				{data: JSON.stringify(request)}).done(function(response)
				{
					if (response == "True")
					{
						window.location = "textReader.html";
					}
					else{
						status_msg("Password not matched")
					}
				});
		}
}



function validate_passwd(passwd)
{
	/* Incomplete Code for password format validation 
	 * password validation Regex will be here
	 * Right now i dont know how the password should be so returning true for now 
	 */
	return true;
}




/* function to print please wait in status msg*/
function please_wait()
{
		status_msg("please wait...");
}


/* function to show message status msg*/
function status_msg(msg)
{
		document.getElementById("status-msg").innerHTML = msg;
}