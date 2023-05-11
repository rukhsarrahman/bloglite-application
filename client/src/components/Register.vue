<template>
  <div class ="New-user">
    <div class ="user">
      <b-form @submit="onSubmit" class = "New-user-form">
        <div class = "img-reg">
              <img src="../../../static/images/Home.png" alt="">
        </div>
        <div class ="form-reg">
          <h2 class ="header-reg">Create Your account</h2>
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
            class = "input">
          </b-form-input>
        </b-form-group>
        <b-form-group
        id="input-group-2"
        label="Password:"
        label-for="password"
        class ="label">
          <b-form-input
            id="password"
            type="password"
            v-model="form.password"
            placeholder="Enter password"
            required
            class = "input">
          </b-form-input>
          </b-form-group>
        <b-form-group
        id="input-group-3"
        label="Username:"
        label-for="username"
        class ="label">
          <b-form-input
            id="username"
            type="username"
            v-model="form.username"
            placeholder="Enter username"
            required
            class="input">
          </b-form-input>
        </b-form-group>
        <b-form-group
        id="input-group-4"
        label="Name:"
        label-for="name"
        class ="label">
          <b-form-input
            id="name"
            type="name"
            v-model="form.name"
            placeholder="Enter name"
            required
            class="input"
          ></b-form-input>
        </b-form-group>
        <div class ="login-link">
          <b-link href="http://localhost:8081/" style="color: rgb(0, 0, 18);
          font-weight: bold;">Already have an account?</b-link>
        </div>
        <b-button
        type="submit"
        variant="primary"
        class ="button">Create</b-button>
        </div>
      </b-form>
    </div>
  </div>
</template>

<script>
import CustomFetch from './CustomFetch';
/* eslint-disable */
  export default {
      name: 'RegisterProfile',
    data() {
      return {
        form: {
          email: '',
          password: '',
          username: '',
          name: ''
        },
      }
    },
    methods: {
      onSubmit(event) {
          event.preventDefault()
          CustomFetch("http://localhost:8080/user", {
              method: 'POST',
              mode: 'cors',
              body: JSON.stringify(this.form),
              headers: {
                  'Content-Type': 'application/json',
              },
          })
          .then((data)=> {
              this.$router.push({path: '/'})
          })
          .catch((err) => {
              alert("An error occured")
          })
      },
    }
  }
</script>
<style>
.New-user{
background-image: url("../../../static/images/login-back.png");
background-size: cover;
background-position: cover;
background-size: cover;
}
.user{
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;
height: 100vh;
}
.img-reg{
  display:flex;
  height: 450px;
  padding-left: 0%;
}
.form-reg{
  display:inline;
  height: 700px;
  width: 600px;
  justify-content: center;
  padding-left: 60px;
  padding-top: 4%;
}
.header-reg{
font-size: 2rem;
color:white;
margin-bottom: 2rem;
padding-left: 50px;
}
.New-user-form{
display: flex;
background-color:linear-gradient(135deg, rgba(255,255,255.0.1), rgba(255,255,255,0));
backdrop-filter: blur(10px);
width: 100%;
height: 100%;
padding: 2rem;
border-radius: 10px;
align-items: center;
border-radius: 5px;
box-shadow: 0px 0px 50px rgba(2, 2, 2, 0.5);
}
.label{
margin-bottom: 1.5rem;
color: white;
}
.input{
border-radius: 5px;
}
.button {
width: 100%;
margin-top: 1.5rem;
}
</style>