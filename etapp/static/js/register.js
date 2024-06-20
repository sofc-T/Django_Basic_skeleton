
const userNameField = document.querySelector("#UserNameField");
const emailField = document.querySelector("#emailField");
const submitButton = document.querySelector("#register");


userNameField.addEventListener('keyup',(e) =>{
    


    userNameVal= e.target.value;
    if (userNameVal.length > 0){
        userNameField.style.borderColor='green';

        fetch('/auth/validateUsername',{
            body:JSON.stringify({
                userName :userNameVal
            }),
            method:"POST",

        })
        .then(res=>res.json())
        .then(data=>{
            
            if (data["usernameError"]){
                submitButton.setAttribute('disabled','disabled');
                // submitButton.disabled = true;
                userNameField.style.borderColor = 'red';
                
            } else {
                submitButton.removeAttribute('disabled');
                // submitButton.disabled = false
            }
        });
    }

})


emailField.addEventListener('keyup',(e)=>{
    emailVal = e.target.value;
    emailField.style.borderColor='green';
    if (emailVal.length){
        fetch('/auth/validateEmail',{
            body:JSON.stringify({
                email:emailVal
            }),
            method:'POST'
        })
        
        .then(res=>res.json())
        .then(data=>{

            if (data["emailError"]){
                submitButton.setAttribute('disabled','disabled');
                // submitButton.disabled = true;
                emailField.style.borderColor='red';
            } else {
                submitButton.removeAttribute('disabled');
                // submitButton.disabled = false;
            }
        })
    }
})