$(document).ready(function() {

$("#signup_pin_gen").click(function() {
  window.location = "user-signup.html";
});

$("#home-button").click(function() {
  window.location = "user-login.html";
});

$("#user-submit-button").click(function() {
    login();
    window.location = "../textReader.html";
});

$("#signup-button").click(function() {
    userSignup();
    window.location = "user-login.html";

});


function userSignup() {
  var  userName = $("#fname").val();
  var  contactDetails = $("#contactNo").val();
  var  pwd = $("#pwd").val();
  var  cpwd = $("#cpwd").val();
  var  contactDetails = $("#contactNo").val();
  if(pwd !=cpwd) {
    alert("password is not match");
    return;
  }
  else {
        var request = {}
        request["userName"] = userName;
        request["contactDetails"] = contactDetails;
        request["pwd"] = pwd;
        request["cpwd"] = cpwd;
  }

}

});
