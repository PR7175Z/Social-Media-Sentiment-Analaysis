document.addEventListener('DOMContentLoaded', () => {
    function capitalizeFirstLetter(val) {
        return String(val).charAt(0).toUpperCase() + String(val).slice(1);
    }

    async function get_response(inputtext) {
        const features = {'text': inputtext}

        const api = 'http://127.0.0.1:2000/predict';
        const response = await fetch(api,{
                method : 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body:JSON.stringify(features)
            }
        )

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    }

    document.getElementById('inputForm').addEventListener('submit', (e) => {
        e.preventDefault();

        const inputValue = document.querySelector('textarea[name="caption"]').value;

        async function displayResponse() {
            try {
                let response = await get_response( inputValue);

                document.querySelector('.result').innerHTML = capitalizeFirstLetter(response);
            } catch (error) {
                console.error("Error:", error);
            }
        }

        displayResponse();
    })
})