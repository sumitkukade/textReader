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
				"login.py/login",
				{data: JSON.stringify(request)}).done(function(response)
				{
					if (response == "True")
					{
						alert("true");
					}
					else{
						alert("false");
					}
								

				});

		}
		alert(passwd);
}



function validate_passwd(passwd)
{
	return true;
}




/* function to print please wait in status msg*/
function please_wait()
{
		status_msg("status-msg","please wait...")
}


/* function to print anything in status msg*/
function status_msg(id,msg)
{
		document.getElementById(id).innerHTML = msg;
}