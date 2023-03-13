<template>
  <div>
    <div>
      <b-navbar type="dark" variant="dark">
        <b-navbar-nav style="padding: 25px;">
          <b-nav-item style="position: absolute; top: 5%;">
              <h2>BlogLite</h2></b-nav-item>
          <b-nav-item @click="goHome()" style="position: absolute; top: 18%; left: 80%;">
              <i class="bi bi-house"></i> Home</b-nav-item>
            <b-nav-item-dropdown text= "Profile" left
            style="position: absolute; top: 18%; left: 88%;">
              <b-dropdown-item @click="goEdit()"><i class="bi bi-gear">
              </i> Edit Profile</b-dropdown-item>
              <b-dropdown-item href="#"><i class="bi bi-box-arrow-right"></i>
                Logout</b-dropdown-item>
            </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-navbar>
    </div>
    <h5 style="padding-top: 5%; padding-left: 30%; padding-right: 30%;">Edit User Details</h5>
    <form style="padding-top: 1%; padding-left: 30%; padding-right: 30%;">
          <div class="form-group">
            <h5>Name</h5>
            <input
            v-model="name"
            type="text" class="form-control"
            id="Name"
            aria-label="Name">
          </div>
          <br>
          <div class="form-group">
            <h5>Bio</h5>
            <input
            v-model="bio"
            type="text" class="form-control"
            id="BIo"
            aria-label="BIo">
          </div>
          <br>
          <div class="form-group">
            <h5>Email</h5>
            <input
            v-model="email"
            type="email" class="form-control"
            id="Email"
            aria-label="Email">
          </div>
          <br><div class="form-group">
            <h5>Password</h5>
            <input
            v-model="password"
            type="password" class="form-control"
            id="Password"
            aria-label="Password">
          </div>
          <br>
          <div class="form-group">
            <h5>Profile Photo</h5>
            <input type="file"
            @change="getFileName"
            class="form-control-file"
            id="profile_photo_input"
            aria-label="Post_Photo">
          </div>
          <br>
          <button type="submit" class="btn btn-primary" @click="onSubmit">Submit</button>
        </form>
  </div>
</template>

<script>
/* eslint-disable */
import CustomFetch from './CustomFetch';
export default {
  name: 'User',
  data() {
    return {
      username: '',
      name: '',
      bio: '',
      profile_photo:'',
      email: '',
      password: '',
    }
    },
    mounted() {
      this.getUser();
    },
    methods: {
      getUser() {
        CustomFetch('http://localhost:8080/user/*', {
          method: 'GET',
          mode: 'cors',
        })
        .then((res) => {
          this.username = res.username;
          this.name = res.name;
          this.bio = res.bio;
          this.email = res.email;
          this.password = res.password;
          this.profile_photo = res.profile_photo;
        })
        .catch((error) => {
          console.error(error);
        });
      },
      goHome() {
        this.$router.push({path:'/dashboard'});
        this.$router.go();
      },
    onSubmit(){
      const payload = {
            username: this.username,
            name: this.name,
            bio: this.bio,
            profile_photo: this.profile_photo,
            email: this.email,
            password: this.password,
          };
          this.update(payload);
    },
    update(payload) {
      CustomFetch("http://localhost:8080/user", {
                method: 'PUT',
                body: JSON.stringify(payload),
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
        .then(() => {
          this.goHome();
        })
        .catch((error) => {
          console.log(error);
          this.goHome();
        });
        this.goHome();
    },
    getFileName() {
        this.profile_photo = document.getElementById("profile_photo_input").value.split("\\").at(-1);
        console.log(this.profile_photo)
      },
      goEdit() {
        this.$router.push({path:'/profilesettings'})
      }
    } 
  }
</script>

<style>
#profile {
position: fixed;
font-size: 10px;
top: 15%;
left: 5%;
padding: 15px;
background-color: lavender;
}

#posts {
  padding: 10px;
  margin-top: 6%;
  margin-left: 35%;
}

.card{
  margin-bottom: 12px;
}

</style>
