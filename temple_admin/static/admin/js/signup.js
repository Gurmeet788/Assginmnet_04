const signupForm = document.getElementById("signupForm");
const message = document.getElementById("message");

signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword =
        document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {
        message.textContent = "Passwords do not match.";
        return;
    }

    try {
        const response = await fetch("/auth/sigup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent = data.error || "Signup failed";
            return;
        }

        message.textContent = "Signup successful!";
        signupForm.reset();

    } catch (error) {
        console.error(error);
        message.textContent = "Something went wrong.";
    }
});