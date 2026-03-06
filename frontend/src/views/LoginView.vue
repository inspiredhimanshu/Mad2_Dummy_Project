<template>
    <div class="container-fluid">
        <div class="row justify-content-centre">
            <div class="col-6">
                <h1 class = "text-centre">Login</h1>
                <form v-on:submit.prevent="login">
                    <div class="mb-3">
                        <label for="exampleInputEmail1" class="form-label">Email address</label>
                        <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" v-model="email">
                    </div>
                    <div class="mb-3">
                        <label for="exampleInputPassword1" class="form-label">Password</label>
                        <input type="password" class="form-control" id="exampleInputPassword1" v-model="password" @input="ValidatePassword">
                        <div id="passwordHelp" class="form-text" style="color: red;">{{ passwordError }}</div>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                    </form>
            </div>
        </div>
    </div>
</template>


<script setup>
import {ref} from 'vue';

const email = ref('');
const password = ref('');

const passwordError = ref('');

function ValidatePassword(){
    if (password.value.length < 6) {
        passwordError.value = 'Password must be at least 6 characters long.';
        return false;
        }
        else {
            passwordError.value = '';
            return true;
        }
}


async function login(){
    if (!ValidatePassword()) {
        alert('Invalid Password Length.');
        return;
    }
    if (email.value === '' || password.value === '') {
        alert('Please fill in all fields.');
        return;
    }

    const response = await fetch("http://127.0.0.1:5000/api/login", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email.value,
            password: password.value
        })
    });
    console.log(response);

    if (!response.ok) {
        const errorData = await response.json();
        console.error(errorData);
        alert(`Login failed: ${errorData.message}`);
        return;
    } else{
        const data = await response.json();
        console.log(data);
        // alert(`Login successful: ${data.message}`);

        localStorage.setItem('token', data.user.auth_token);
        // localStorage.removeItem('token')
        alert(`Login successful: ${data.message}`);
        return;
    }

}
</script>