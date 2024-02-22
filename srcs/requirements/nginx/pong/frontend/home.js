
function showHome() {
    let usernameInput;
    let passwordInput;
    var mainElement = document.getElementById('content');
    mainElement.innerHTML = '<h1>Welcome to Pong!</h1>';
    mainElement.innerHTML += '<div id="login">' + 
    '<form id="loginForm1" style="display: flex; flex-direction: column; align-items: center;">' +
    '<p style="padding-top: 2em; display: flex; align-items:center; justify-content:center;" > Username: </p>' +
    '<input type="text" id="usernameInputid">' +  // Corrected ID here
    '<button type="submit" class="styled-button" style="margin-top: 1em;">Submit</button>' +
    '</form>' +
    '</div>';
    
    const submit1 = mainElement.querySelector('#loginForm1');
    const input1 = mainElement.querySelector('#usernameInputid'); // Corrected ID here

    submitButton(submit1).then(isSubmitted => {
        if (isSubmitted === true && input1.value !== "") {
            usernameInput = input1.value;
            mainElement.querySelector('#login').remove();
            showPasswordForm();
        }
    });

    function showPasswordForm() {
        var mainElement = document.getElementById('content');
        mainElement.innerHTML += '<div id="login">' + 
        '<form id="loginForm2" style="display: flex; flex-direction: column; align-items: center;">' +
        '<p style="padding-top: 2em; display: flex; align-items:center; justify-content:center;" > Password: </p>' +
        '<input type="password" id="passwordInput">' +
        '<button type="submit" class="styled-button" style="margin-top: 1em;">Submit</button>' +
        '</form>' +
        '</div>';
        
        const submit2 = mainElement.querySelector('#loginForm2');
        const input2 = mainElement.querySelector('#passwordInput');
        
        submitButton(submit2).then(isSubmitted => {
            if (isSubmitted === true && input2.value !== "") {
                passwordInput = input2.value;
                mainElement.querySelector('#login').remove();
                checkLogin();
            }
        });
    
    }
    
    function checkLogin() {
        console.log(usernameInput);
        console.log(passwordInput);
        if (usernameInput !== undefined && passwordInput !== undefined) {
            var mainElement = document.getElementById('content');
            mainElement.innerHTML = '<h2 style="align-text:center;"> Well done, you are logged in !</h2>';
        }
    }
}


function submitButton(form) {
    return new Promise(function(resolve) {
        form.addEventListener("submit", function(event) {
            event.preventDefault(); // Prevent the default form submission behavior
            resolve(true);
        });
    });
}













































// var mainElement = document.getElementById('content');
// mainElement.innerHTML = '<h1>Welcome to Pong!</h1>';
// const title = document.getElementById('title');
// let ballTriggered = 1;
// if (ballTriggered == 1) {
// title.addEventListener("mouseenter", function() {
//     var numBalls = 42;
//     const windowHeight = window.innerHeight;
//     const windowWidth = window.innerWidth;
//     const rangeTop = windowHeight * 0.02; 
//     const rangeBottom = windowHeight * 0.14; 
//     const leftMin = windowWidth * 0.2; // Minimum left position (40% of window width)
//     const leftMax = windowWidth * 0.60; // Maximum left position (60% of window width)

//     for (let i = 1; i <= numBalls; i++) {
//         const ball = document.createElement("div");
//         ball.className = "ball";
        
//         // Generate random positions within specified ranges
//         const randomTop = rangeTop + Math.random() * (rangeBottom - rangeTop);
//         const randomLeft = leftMin + Math.random() * (leftMax - leftMin);
        
//         ball.style.top = `${randomTop}px`; // Adjust top position
//         ball.style.left = `${randomLeft}px`; // Adjust left position
//         ball.style.zIndex = -1; // Set z-index to place the ball behind other elements
//         ball.style.animationDelay = `${i * 0.04}s`; // Delay animation for each ball
//         title.appendChild(ball);
//     }
// });
// title.addEventListener("mouseleave", function() {
//     const balls = title.querySelectorAll(".ball");
//     balls.forEach(function(ball) {
//         numballs = 0;
//         ball.remove();
//         ball.delete
//     });
// });
// }
// ballTriggered = 0;
// title.removeEventListener("mouseenter", handleMouseEnter);
// title.removeEventListener("mouseleave", handleMouseLeave);