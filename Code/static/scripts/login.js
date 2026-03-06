document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const payload = {
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        };

        try {
            const response = await fetch("/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                console.log("Connexion réussie");
                alert(data.reponse);
                // Exemple : redirection
                // window.location.href = "/";
            } else {
                alert(data.reponse);
            }

        } catch (error) {
            console.error("Erreur réseau :", error);
            alert("Erreur de connexion au serveur");
        }
    });
});
