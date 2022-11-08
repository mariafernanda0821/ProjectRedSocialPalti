const fileTypes = [
  	"image/apng",
	 "image/bmp",
  	"image/gif",
  	"image/jpeg",
  	"image/pjpeg",
  	"image/png",
  	"image/svg+xml",
  	"image/tiff",
  	"image/webp",
  	"image/x-icon"
	];
	function validFileType(file) {
	  	return fileTypes.includes(file.type);
	}

	function returnFileSize(number) {
  		if (number < 1024) {
	    	return `${number} bytes`;
  		} else if (number >= 1024 && number < 1048576) {
	    	return `${(number / 1024).toFixed(1)} KB`;
  		} else if (number >= 1048576) {
    		return `${(number / 1048576).toFixed(1)} MB`;
  		}
	}

	
	// timeout before a callback is called
    let timeout;
    // traversing the DOM and getting the input and span using their IDs
    let strengthBadge = document.getElementById('StrengthDisp')
    // The strong and weak password Regex pattern checker
    let strongPassword = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
    let mediumPassword = new RegExp("^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{6,})");
    
    function StrengthChecker(PasswordParameter){
        // We then change the badge's color and text based on the password strength
        if(strongPassword.test(PasswordParameter)) {
            strengthBadge.style.backgroundColor = "green"
            strengthBadge.textContent = 'Strong'
        } else if(mediumPassword.test(PasswordParameter)){
            strengthBadge.style.backgroundColor = '#eaab4a'
            strengthBadge.textContent = 'Medium'
        } else{
            strengthBadge.style.backgroundColor = 'red'
            strengthBadge.textContent = 'Weak'
        }
    }
	
    function validateEmail(){
                
	// Get our input reference.
	var emailField = document.getElementById('useremail');
	
	// Define our regular expression.
	var validEmail =  /^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$/;

	// Using test we can check if the text match the pattern
	if( validEmail.test(emailField.value) ){
		alert('Email is valid, continue with form submission');
		return true;
	}else{
		alert('Email is invalid, skip form submission');
		return false;
	}
	} 

document.getElementById('userpasswd').addEventListener("input", () => {
	        //The badge is hidden by default, so we show it

        strengthBadge.style.display= 'block'
        clearTimeout(timeout);

        //We then call the StrengChecker function as a callback then pass the typed password to it

        timeout = setTimeout(() => StrengthChecker(document.getElementById('userpasswd').value), 500);

        //Incase a user clears the text, the badge is hidden again

        if(document.getElementById('userpasswd').value.length !== 0){
            strengthBadge.style.display != 'block'
        } else{
            strengthBadge.style.display = 'none'
        }
});

document.querySelector("#userprofile").onchange = function(event) {
		let archivo = event.target.files[0];
		if(archivo.length === 0) {
			console.log("No seleciono el avatar");
		} else {
			if(validFileType(archivo)) {
				let vista =  document.querySelector("#vista-userprofile");
				vista.src = URL.createObjectURL(archivo);
				console.log(returnFileSize(archivo.size));
			} else {
				console.log("Tipo de archivo no valido");
			}
		}
	}