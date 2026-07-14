


 Swal.fire({

            icon: '{% if message.tags == "success" %}success{% elif message.tags == "error" %}error{% elif message.tags == "warning" %}warning{% else %}info{% endif %}',

            title: '{{ message.tags|title }}',

            text: '{{ message }}',

            timer: 2000,

            showConfirmButton: false

        });

