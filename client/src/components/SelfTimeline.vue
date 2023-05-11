<template>
  <div class="SelfTimeline">
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
        </b-navbar-nav>
      </b-navbar>
    </div>
      <div id="profile-dash" class="profile-card"  style="width: 16rem;">
          <img class="card-img-top rounded-circle" style="width: 6cm; height: 6cm;"
          v-bind:src="require('../../../static/images/' + user.profile_photo)"
          width="200" height="200" alt="profile photo" />
          <div class="card-body">
              <h5 class="card-title">{{ user["name"] }}</h5>
              <b-link @click="$event=>toTimeline(user.username)"
                style="font-weight: bold;color: white; font-size: medium;">
              @{{ user["username"] }}</b-link><br><br>
              <h7>Followers: {{ user["followers"] }}</h7><br>
              <p class="card-text">{{ user['bio'] }}</p>
          </div>
      </div>
      <div id="posts">
          <div class="col">
              <div class="card" v-for="post in posts" :key="post" style="width: 40rem;">
                  <div class="card-body">
                  <img class="rounded-circle" style="width: 1cm; height: 1cm;"
          v-bind:src="require('../../../static/images/' + post.user.profile_photo)"
          alt="post photo" />
             <b-link @click="$event=>toTimeline(user.username)"
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
                  <b-button v-if="!likes.includes(post.post_id)"
                  variant="default" @click="likePost(post.post_id)">
                    <strong><i class="bi bi-hand-thumbs-up"></i>
                      Like({{ post["likes_num"]  }})</strong></b-button>
                    <b-button v-else
                  variant="primary" @click="unlikePost(post.post_id)">
                    <strong><i class="bi bi-hand-thumbs-up"></i>
                      Liked({{ post["likes_num"] }})</strong></b-button>
                  <b-button variant="default" @click="toPost(post.post_id)">
                    <strong><i class="bi bi-chat"></i>
                      Comment({{ post["comments_num"]  }})</strong></b-button>
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
  </div>
</template>

<script>
/* eslint-disable */
import CustomFetch from './CustomFetch';
export default {
  name: 'SelfTimeline',
  data() {
    return {
      likes:[],
      view_user: window.location.pathname.split("/").at(-1),
      user: [],
      posts: [],
      commentForm: {
          post_id: null,
          body: '',
          commenter: null,
      }
    }
    },
    mounted() {
      this.getLikes();
      this.getUser();
      this.getFollows();
      this.getPost();
    },
    methods: {
      getLikes() {
        CustomFetch('http://localhost:8080/like/*', {
          method: 'GET',
          mode: 'cors',
        })
        .then((res) => {
          console.log(res)
          for(let i = 0; i < res.length; i++) {
            this.likes.push(res[i]["post_id"])
          }
          console.log(this.likes)
        })
        .catch((error) => {
          console.error(error);
        });
      },
      getFollows() {
        CustomFetch('http://localhost:8080/follow/*', {
          method: 'GET',
          mode: 'cors',
        })
        .then((res) => {
          for(let i = 0; i < res.length; i++) {
            if(res[i].following == this.user.username) {
              this.follow = true
              break
            }
          }
        })
        .catch((error) => {
          console.error(error);
        });
      },
      getUser() {
        CustomFetch('http://localhost:8080/user/'+this.view_user, {
          method: 'GET',
          mode: 'cors',
        })
        .then((res) => {
          this.user = res;
        })
        .catch((error) => {
          console.error(error);
        });
      },
      getPost() {
        CustomFetch('http://localhost:8080/post/'+this.view_user, {
          method: 'GET',
          mode: 'cors',
        })
        .then((res) => {
          this.posts = res;
          this.posts = this.posts.reverse()
        })
        .catch((error) => {
          console.error(error);
        });
      },
    toUser(username) {
      console.log(username)
    },
    toPost(post_id) {
      this.$router.push({path:'/posts/'+post_id})
    },
    goHome() {
      this.$router.push({path:'/dashboard'})
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
        console.error(error);
        this.getLikes();
        this.getUser();
        this.getPost();
      });
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
        this.getLikes();
        this.getUser();
        this.getPost();
      })
      .catch((error) => {
        console.log(error);
        this.getUser();
        this.getLikes();
        this.getPost();
      });
    },
    toPost(post_id) {
      this.$router.push({path:'/posts/'+post_id})
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
    initForm() {
    this.createPost.title = '';
    this.createPost.description = '';
    },
    toTimeline() {
      this.$router.push({path:'/timeline/'+this.user.username})
    },
    } 
  }
</script>

<style>
.SelfTimeline {
  background-image: url("../../../static/images/login-back.png");
  background-size: cover;
  height: 100%;
}
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
#profile-dash{
position: fixed;
font-size: 10px;
top: 15%;
left: 5%;
color: white;
padding: 15px;
box-shadow: 0px 0px 10px rgba(213, 121, 121, 5);
}

</style>
