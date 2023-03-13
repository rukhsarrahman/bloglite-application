<template>
    <div>
      <b-form @submit="onSubmit">
        <b-form-group
          id="input-group-1"
          label="Email address:"
          label-for="email">
          <b-form-input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="Enter email"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-2" label="Password:" label-for="password">
          <b-form-input
            id="password"
            type="password"
            v-model="form.password"
            placeholder="Enter password"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-3" label="Username:" label-for="username">
          <b-form-input
            id="username"
            type="username"
            v-model="form.username"
            placeholder="Enter username"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-4" label="Name:" label-for="name">
          <b-form-input
            id="name"
            type="name"
            v-model="form.name"
            placeholder="Enter name"
            required
          ></b-form-input>
        </b-form-group>
        <div>
          <b-link href="http://localhost:8081/">Already have an account?</b-link>
        </div>
        <b-button type="submit" variant="primary">Submit</b-button>
      </b-form>
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