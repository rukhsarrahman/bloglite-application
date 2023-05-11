<template>
  <div class ="login-back">
    <div class = "login">
      <b-form @submit="onSubmit" class = "login-form">
        <div class = "img">
          <img src="../../../static/images/social.png" alt="">
        </div>
        <div class ="form">
          <h2 class = "header">Log in to your account</h2>
          <b-form-group
            id="input-group-1"
            label="Email address:"
            label-for="email"
            class="label">
            <b-form-input
              id="email"
              v-model="form.email"
              type="email"
              placeholder="Enter email"
              required
              class="input"
            ></b-form-input>
          </b-form-group>
          <b-form-group
          id="input-group-2"
          label="Password:"
          label-for="password"
          class="label">
            <b-form-input
              id="password"
              type="password"
              v-model="form.password"
              placeholder="Enter password"
              required
              class="input"
            ></b-form-input>
          </b-form-group>
          <div class="register-link">
            <b-link href="http://localhost:8081/register" style="color: rgb(27, 142, 224);">New User?</b-link>
          </div>
          <b-button type="submit" variant="primary" class = "button">LOG IN</b-button>
      </div>
      </b-form>
    </div>
  </div>
</template>

<script>
import CustomFetch from './CustomFetch';
/* eslint-disable */
  export default {
      name: 'LoginProfile',
    data() {
      return {
        form: {
          email: '',
          password: '',
        },
      }
    },
    methods: {
      onSubmit(event) {
          event.preventDefault()
          CustomFetch("http://localhost:8080/login", {
              method: 'POST',
              mode: 'cors',
              body: JSON.stringify(this.form),
              headers: {
                  'Content-Type': 'application/json',
              },
          })
          .then((data)=> {
              this.$router.push({path: '/dashboard'})
          })
          .catch((err) => {
              alert("Wrong Credentials")
          })
      },
    }
  }
</script>
<style>
.login-back{
  background-image: url("../../../static/images/login-back.png");
  background-size: cover;
  background-position: center;
  background-size: cover;
}
.login {
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;
height: 100vh;

}
.img{
  display:flex;
  height: 550px;
  padding-left: 0%;
}
.form{
  display:inline;
  height: 600px;
  width: 500px;
  justify-content: center;
  padding-left: 60px;
  padding-top: 10%;
}
.header {
font-size: 2rem;
color:white;
margin-bottom: 2rem;
}

.login-form {
display: flex;
background-color:linear-gradient(135deg, rgba(255,255,255.0.1), rgba(255,255,255,0));
backdrop-filter: blur(10px);
width: 1000px;
height: 600px;
padding: 2rem;
border-radius: 10px;
align-items: center;
border-radius: 5px;
box-shadow: 0px 0px 50px rgba(2, 2, 2, 0.5);
}
.label {
margin-bottom: 1.5rem;
color: white;
}

.input {
border-radius: 5px;
}

.button {
width: 100%;
margin-top: 1.5rem;
}
</style>