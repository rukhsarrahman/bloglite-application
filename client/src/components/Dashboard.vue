<template>
    <div @click="modal=false" @keydown="modal=true">
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
              <b-dropdown-item @click="logout()"><i class="bi bi-box-arrow-right"></i>
                Logout</b-dropdown-item>
            </b-nav-item-dropdown>
            <b-nav-item style="position: absolute; top: 10%; left: 35%;">
                <input type="text" autocomplete="off"
                id="searchUser"
                v-model="people"
                @input="filterPeople"
                @focus="modal=true"
                placeholder="Search for Users"
                style="height: 40px; width: 10cm;"
                aria-label="Search">
                &nbsp;
                <div v-if="filteredPeople && modal">
                  <ul class="list-group" style="width: 8cm;">
                    <li class="list-group-item list-group-item-light"
                    style="z-index: 999;"
                    v-for="filteredPerson in filteredPeople" :key="filteredPerson"
                    @click="setPerson(filteredPerson)" aria-hidden="true">
                      {{ filteredPerson }}</li>
                  </ul>
                </div>
            </b-nav-item>
            <b-navbar-item style="position: absolute; top: 20%; left: 67%;">
              <button class="btn btn-outline-success my-3 my-sm-0" @click="toUser(people)">
                  <i class="bi bi-search"></i> Search</button>
            </b-navbar-item>
          </b-navbar-nav>
        </b-navbar>
      </div>

        <div id="profile" class="card">
            <img class="card-img-top rounded-circle"
            v-bind:src="require('../../../static/images/' + user.profile_photo)"
            width="200" height="200" alt="profile photo" />
            <div class="card-body">
                <h5 class="card-title">{{ user["name"] }}</h5>
                <h7>@{{ user["username"] }}</h7><br><br>
                <p class="card-text">{{ user['bio'] }}</p>
            </div>
        </div>
        <div id="posts">
            <div class="col">
                <div class="card" v-for="post in posts" :key="post" style="width: 40rem;">
                    <div class="card-body">
                    <img class="rounded-circle" style="width: 1cm;"
            v-bind:src="require('../../../static/images/' + post.user.profile_photo)"
            alt="post photo" />
               <b-link @click="$event=>toUser(post.username)"
                style="font-weight: bold; font-size: medium; color: black;">
                @{{ post["username"] }}</b-link>
                <b-dropdown id="dropdown-right" text="⋮"
                variant="default" class="m-2">
                <b-dropdown-item @click="deletePost(post.post_id)">Delete</b-dropdown-item>
              </b-dropdown>

                <br><br>
                    <img class="card-img-top" id="poster"
            v-bind:src="require('../../../static/images/' + post.post_photo)"
            alt="post photo" /><br><br>
                    <b-link @click="toPost(post.post_id)"
                    style="font-weight: bold; font-size: large; color: black;"
                    class="card-title">{{post["title"]}}</b-link>
                    <p class="card-text">{{post["description"]}}</p>
                </div>
                </div>
            </div>
        </div>
        <div class="fixed-bottom d-flex justify-content-end" style="bottom:20px; right: 20px;">
        <button type="button" class="btn btn-primary btn-md rounded-pill"
              v-b-modal.create-post-modal style="font-weight: bold;">
              <i class="bi bi-pen"></i> Create Post</button>
        </div>
        <b-modal ref="createPostModal"
        id="create-post-modal"
        title="Create a Post"
        hide-footer>
        <form>
          <div class="form-group">
            <h5>Title</h5>
            <input
            v-model="title"
            type="text" class="form-control"
            id="Title"
            placeholder="Enter a Title"
            aria-label="Title">
          </div>
          <br>
          <div class="form-group">
            <h5>Description</h5>
            <input type="text"
            v-model="description"
            class="form-control"
            id="Description"
            placeholder="Enter a Description"
            aria-label="Description">
          </div>
          <br>
          <div class="form-group">
            <h5>Enter an Image</h5>
            <input type="file"
            @change="getFileName"
            class="form-control-file"
            id="post_photo_input"
            aria-label="Post_Photo">
          </div>
          <br>
          <button type="submit" class="btn btn-primary" @click="onSubmit">Post!</button>
        </form>
      </b-modal>
      <i class="bi bi-three-dots-vertical"></i>
    </div>
  </template>

<script>
/* eslint-disable */
import { BButton, BModal, VBModal } from "bootstrap-vue";
import CustomFetch from './CustomFetch';
  export default {
    name: 'Dashboard',
    data() {
      return {
        user: [],
        posts: [],
        title:'',
        description:'',
        post_photo:'n',
        all:[],
        people:'',
        modal: false,
        filteredPeople:[],
      }
      },
      mounted() {
        this.getUser();
        this.getPost();
        this.allUsers();
      },
      methods: {
        getUser() {
          CustomFetch('http://localhost:8080/user/*', {
            method: 'GET',
            mode: 'cors',
          })
          .then((res) => {
            this.user = res;
          })
          .catch((error) => {
            console.error(error);
            this.$router.push({path:'/'})
          });
          console.log("hi");
        },
        getPost() {
          CustomFetch('http://localhost:8080/post/timhenson', {
            method: 'GET',
            mode: 'cors',
          })
          .then((res) => {
            this.posts = res;
            this.posts = this.posts.reverse();
          })
          .catch((error) => {
            console.error(error);
          });
        },
      toUser(username) {
        this.$router.push({path:'/users/'+username})
      },
      toPost(post_id) {
        this.$router.push({path:'/posts/'+post_id})
      },

      initForm() {
      this.createPost.title = '';
      this.createPost.description = '';
      },

      onSubmit() {
        const payload = {
            title: this.title,
            description: this.description,
            post_photo: this.post_photo,
            username: this.user.username,
          };
          this.addPost(payload);
          this.initForm()
      },

      addPost(new_post) {CustomFetch("http://localhost:8080/post", {
                method: 'POST',
                body: JSON.stringify(new_post),
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
        .then(() => {
          this.getUser();
          this.getPost();
        })
        .catch((error) => {
          console.log(error);
          this.getUser();
          this.getPost();
        });
      },
      getFileName() {
        this.post_photo = document.getElementById("post_photo_input").value.split("\\").at(-1);
      },
      deletePost(post_id) {
        CustomFetch(`http://localhost:8080/post/${post_id}`, {
          method: 'DELETE',
          mode: 'cors',
          headers: {
            'Content-type': 'application/json',
          },
        })
        .then(() => {
          this.getUser();
          this.getPost();
        })
        .catch((error) => {
          console.error(error);
          this.getUser();
          this.getPost();
        });
      },
      goHome() {
        this.$router.push({path:'/dashboard'})
      },
      allUsers() {
        CustomFetch('http://localhost:8080/all', {
            method: 'GET',
            mode: 'cors',
          })
          .then((res) => {
            for(let i = 0; i < res.length; i++) {
              this.all.push(res[i]["username"])
            }

          })
          .catch((error) => {
            console.error(error);
          });
      },

      filterPeople() {
        this.filteredPeople = this.all.filter(people => {
          return people.toLowerCase().startsWith(this.people.toLocaleLowerCase())
        })
      },
      setPerson(person) {
        this.people = person;
        this.modal = false;
      },
      goEdit() {
        this.$router.push({path:'/profilesettings'})
      },
      logout() {
        CustomFetch('http://localhost:8080/logout', {
            method: 'GET',
            mode: 'cors',
          })
          .then((res) => {
            this.$router.push({path:'/'})
          })
          .catch((error) => {
            console.error(error);
          });
      },
      },
      components: {
            BButton,
            BModal
        },

        directives: { 
            'b-modal': VBModal 
        },
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
}

.card{
    margin-bottom: 12px;
}
</style>
