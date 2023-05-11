<template>
  <div class = "Dashboard"
  @click="modal=false" @keydown="modal=true" style="font-family: Arial, sans-serif;">
    <div class="bg-image">
      <b-navbar type="dark" variant="dark">
        <b-navbar-nav style="padding: 25px;">
          <b-nav-item style="position: absolute; top: 5%;left: 3%;">
            <h2>BlogLite</h2></b-nav-item>
          <b-nav-item @click="goHome()" style="position: absolute; top: 18%; left: 80%;">
            <i class="bi bi-house"></i> Home</b-nav-item>
          <b-nav-item-dropdown text= "Profile" left
          style="position: absolute; top: 18%; left: 86%;">
            <b-dropdown-item @click="goEdit()"><i class="bi bi-gear">
            </i> Edit Profile</b-dropdown-item>
            <b-dropdown-item @click="logout()"><i class="bi bi-box-arrow-right"></i>
              Logout</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item style="position: absolute; top: 10%; left: 28%;">
              <input type="text" autocomplete="off"
              id="searchUser"
              v-model="people"
              @input="filterPeople"
              @focus="modal=true"
              placeholder="Search for Users"
              style="height: 40px; width: 13cm;"
              aria-label="Search">
              &nbsp;
              <div v-if="filteredPeople && modal">
                <ul class="list-group" style="width: 15cm;">
                  <li class="list-group-item list-group-item-light"
                  style="z-index: 999;"
                  v-for="filteredPerson in filteredPeople" :key="filteredPerson"
                  @click="setPerson(filteredPerson)" aria-hidden="true">
                    {{ filteredPerson }}</li>
                </ul>
              </div>
          </b-nav-item>
          <b-navbar-item style="position: absolute; top: 20%; left: 68%;">
            <button class="btn btn-outline-success my-3 my-sm-0" @click="toUser(people)"
            style="color: #0be10b;">
                <i class="bi bi-search"></i> Search</button>
          </b-navbar-item>
        </b-navbar-nav>
      </b-navbar>
    </div>
    <div id="profile-dash" class="profile-card" style="width: 16rem;">
      <img class="card-img-top rounded-circle"
      style="width: 6cm; height: 6cm;"
        v-bind:src="require('../../../static/images/' + user.profile_photo)"
        width="200" height="200"
        alt="profile photo" />
      <div class="card-body-profile">
        <h5 class="card-title-profile">{{ user["name"] }}</h5>
        <b-link @click="$event => toTimeline(user.username)"
          style="font-weight: bold;color: white; font-size: medium;">
          @{{ user["username"] }}</b-link><br>
        <p class="card-text" style="font-size: medium;">{{ user['bio'] }}</p>
      </div>
    </div>

    <div>
      <b-tabs horizontal top style="margin-top:4%;margin-left: 30%; margin-right: 15%;">
        <b-tab title="Your Feed" active>
          <div class="col" style="padding-top: 2%;">
            <div class="card-dash" v-for="post in posts" :key="post">
              <div class="card-body-dash">
                <img class="rounded-circle" style="width: 1cm; height: 1cm;"
                  v-bind:src="require('../../../static/images/' + post.user.profile_photo)"
                  alt="post photo" />
                <b-link @click="$event => toUser(post.username)"
                  style="font-weight: bold; font-size: medium; color: black;font-size: 20px;">
                  @{{ post["username"] }}</b-link>
                <br><br>
                <img class="card-img-top" id="poster"
                v-bind:src="require('../../../static/images/' + post.post_photo)"
                  alt="post photo" /><br><br>
                <b-link @click="toPost(post.post_id)"
                style="font-weight: bold; font-size: large; color: black;"
                  class="card-title-dash">{{ post["title"] }}</b-link>
                <p class="card-text-dash">{{ post["description"] }}</p>
                <b-button v-if="!likes.includes(post.post_id)"
                variant="default" @click="likePost(post.post_id)">
                  <strong>
                    <img src="../../../static/images/like.png" alt="like"
                    style="height: 30px; width: 30px;">
                    ({{ post["likes_num"] }})</strong></b-button>
                <b-button v-if="likes.includes(post.post_id)"
                variant="default" @click="unlikePost(post.post_id)">
                  <strong>
                    <img src="../../../static/images/liked.png" alt="liked"
                    style="height: 30px; width: 30px;">
                    ({{ post["likes_num"] }})</strong></b-button>
                <b-button variant="default" @click="toPost(post.post_id)">
                  <strong>
                    <img src="../../../static/images/comment.png" alt="comment"
                    style="height: 30px; width: 30px;">
                    ({{ post["comments_num"] }})</strong></b-button>
              </div>
            </div>
          </div>
        </b-tab>
        <b-tab title="Trending">
          <div class="col" style="padding-top: 2%;">
            <div class="card-dash" v-for="post in trending" :key="post">
              <div class="card-body-dash">
                <img class="rounded-circle" style="width: 1cm; height: 1cm;"
                  v-bind:src="require('../../../static/images/' + post.user.profile_photo)"
                  alt="post photo" />
                <b-link @click="$event => toUser(post.username)"
                  style="font-weight: bold; font-size: medium; color: black; font-size: 20px;">
                  @{{ post["username"] }}</b-link>
                <br><br>
                <img class="card-img-top" id="poster"
                v-bind:src="require('../../../static/images/' + post.post_photo)"
                  alt="post photo" /><br><br>
                <b-link @click="toPost(post.post_id)"
                style="font-weight: bold; font-size: large; color: black;"
                  class="card-title-dash">{{ post["title"] }}</b-link>
                <p class="card-text-dash">{{ post["description"] }}</p>
                <b-button v-if="!likes.includes(post.post_id)"
                variant="default" @click="likePost(post.post_id)">
                  <strong>
                    <img src="../../../static/images/like.png" alt="like"
                    style="height: 30px; width: 30px;">
                    ({{ post["likes_num"] }})</strong></b-button>
                <b-button v-if="likes.includes(post.post_id)"
                variant="default" @click="unlikePost(post.post_id)">
                  <strong>
                  <img src="../../../static/images/liked.png" alt="liked"
                  style="height: 30px; width: 30px;">
                    ({{ post["likes_num"] }})</strong></b-button>
                <b-button variant="default" @click="toPost(post.post_id)">
                  <strong>
                    <img src="../../../static/images/comment.png" alt="comment"
                    style="height: 30px; width: 30px;">
                    ({{ post["comments_num"] }})</strong></b-button>
              </div>
            </div>
          </div>
        </b-tab>
      </b-tabs>
    </div>

    <div class="fixed-bottom d-flex justify-content-end" style="bottom:20px; right: 20px;">
      <button type="button"
      class="btn btn-primary btn-md rounded-pill" v-b-modal.create-post-modal
        style="font-weight: bold;">
        <i class="bi bi-pen"></i> Create Post</button>
    </div>
    <b-modal ref="createPostModal" id="create-post-modal" title="Create a Post" hide-footer>
      <form>
        <div class="form-group">
          <h5>Title</h5>
          <input v-model="title" type="text"
          class="form-control" id="Title"
          placeholder="Enter a Title"
            aria-label="Title">
        </div>
        <br>
        <div class="form-group">
          <h5>Description</h5>
          <input type="text"
          v-model="description" class="form-control"
          id="Description" placeholder="Enter a Description"
            aria-label="Description">
        </div>
        <br>
        <div class="form-group">
          <h5>Enter an Image</h5>
          <input type="file" @change="getFileName" class="form-control-file" id="post_photo_input"
            aria-label="Post_Photo">
        </div>
        <br>
        <button type="submit" class="btn btn-primary" @click="onSubmit">Post!</button>
      </form>
    </b-modal>
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
      likes: [],
      user: [],
      posts: [],
      title:'',
      description:'',
      post_photo:'n',
      all:[],
      people:'',
      modal: false,
      filteredPeople:[],
      trending:[]
    }
    },
    mounted() {
      this.getLikes();
      this.getUser();
      this.getPost();
      this.allUsers();
      this.getTrending();
    },
    methods: {
      getTrending() {
        CustomFetch('http://localhost:8080/trending', {
          method: 'GET',
          mode: 'cors',
        })
        .then((res) => {
          this.trending = res;
        })
        .catch((error) => {
          console.error(error);
        });
      },
      getLikes() {
        CustomFetch('http://localhost:8080/like/*', {
          method: 'GET',
          mode: 'cors',
        })
        .then((res) => {
          this.likes = []
          for(let i = 0; i < res.length; i++) {
            this.likes.push(res[i]["post_id"])
          }
          console.log(this.likes)
        })
        .catch((error) => {
          console.error(error);
        });
      },
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
        CustomFetch('http://localhost:8080/feed', {
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
      if(username == this.user.username)
        this.$router.push({path:'/timeline/'+username})
      else
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

    addPost(new_post) {
      CustomFetch("http://localhost:8080/post", {
              method: 'POST',
              body: JSON.stringify(new_post),
              mode: 'cors',
              headers: {
                  'Content-Type': 'application/json',
              },
          })
      .then(() => {
        this.$router.push({path:'/timeline/'+this.user.username})
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
    unlikePost(post_id) {
      CustomFetch(`http://localhost:8080/like/${post_id}`, {
        method: 'DELETE',
        mode: 'cors',
        headers: {
          'Content-type': 'application/json',
        },
      })
      .then(() => {
        this.getLikes();
        this.getUser();
        this.getPost();
      })
      .catch((error) => {
        this.getLikes();
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
    toTimeline() {
      this.$router.push({path:'/timeline/'+this.user.username})
    },

    likePost(post_id) {
      console.log("post a like")
      const new_like = {"post_id": post_id}
      CustomFetch("http://localhost:8080/like", {
              method: 'POST',
              body: JSON.stringify(new_like),
              mode: 'cors',
              headers: {
                  'Content-Type': 'application/json',
              },
          })
      .then(() => {
        this.getUser();
        this.getLikes();
        this.getPost();
      })
      .catch((error) => {
        console.log(error);
        this.getUser();
        this.getLikes();
        this.getPost();
      });
    }
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
.Dashboard{
background-image: url("../../../static/images/login-back.png");
background-size: cover;
height: 100%;
}
#profile-dash{
position: fixed;
font-size: 10px;
top: 15%;
left: 5%;
color: white;
padding: 15px;
box-shadow: 0px 0px 10px rgba(213, 121, 121, 5);
}
.navbar-nav .nav-link {
font-size: 18px;
color: #0be10b;
}
.card-body-dash{
box-shadow: 0px 0px 10px rgba(2, 2, 2, 0.5);
padding-top: 20px;
padding-left: 10px;
padding-right: 10px;
padding-bottom: 20px;
font-style: oblique;
color: white;
font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
}
</style>
