<template>
  <div class="post">
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
      <div id="profile-post" class="card-post" style="width: 16rem;">
          <img class="card-img-top rounded-circle" style="width: 6cm; height: 6cm;"
          v-bind:src="require('../../../static/images/' + user.profile_photo)"
          width="200" height="200" alt="profile photo" />
          <div class="card-body-post">
              <h5 class="card-title-post">{{ user["name"] }}</h5>
              <h5>@{{ user["username"] }}</h5>
              <p class="card-text" style="font-size: medium;">{{ user['bio'] }}</p>
          </div>
      </div>
      <div id="posts" class="card-post" style="width: 40rem;">
                  <div class="card-body-post">
                  <img class="rounded-circle" style="width: 1cm; height: 1cm;"
          v-bind:src="require('../../../static/images/' + post.user.profile_photo)"
          alt="post photo" />
             <b-link @click="$event=>toUser(post.username)"
              style="font-weight: bold; font-size: large; color: black;">
              @{{ post["username"] }}</b-link><br><br>
                  <img class="card-img-top" id="poster"
          v-bind:src="require('../../../static/images/' + post.post_photo)"
          alt="post photo" /><br><br>
                  <b-link @click="toPost(post.post_id)"
                  style="font-weight: bold; font-size: large; color: black;"
                  class="card-title-post">{{post["title"]}}</b-link>
                  <p class="card-text-post">{{post["description"]}}</p>
              </div>
              <h5>Comments:</h5>
              <ul class="list-group list-group-flush" style="background: fixed;">
              <li class="list-group-item">
                  <textarea v-model="new_comment"
                  placeholder="Post a Comment..." cols="50" aria-label="Comment"></textarea>
                  <button style="font-weight: bold; position: absolute; left:80%; top: 20%;"
                  type="submit" class="btn btn-primary rounded"
                  @click="onSubmit">Submit</button>
              </li>
              <li class="list-group-item" v-for="comment in comments" :key="comment">
                  <img class="rounded-circle" style="width: 1cm; height: 1cm;"
                  v-bind:src="require('../../../static/images/' + comment.user.profile_photo)"
                  alt="post photo" />
                  <b-link @click="$event=>toUser(comment.commenter)"
                      style="font-weight: bold; font-size: medium; color: black;">
                      @{{ comment["commenter"] }}</b-link>
<b-dropdown v-if="comment.commenter == user.username  || post.username == user.username"
                      id="dropdown-right" text="⋮"
                        variant="default" class="m-2">
                        <b-dropdown-item @click="deleteComment(comment.comment_id)">
                          Delete</b-dropdown-item>
                      </b-dropdown>
                      <br>
                      <div style="padding: 2%;">{{ comment['body'] }}</div>
              </li>
          </ul>
          </div>
  </div>
</template>

<script>
/* eslint-disable */
import CustomFetch from './CustomFetch';
export default {
  name: 'Post',
  data() {
    return {
      new_comment:'',
      view_post: window.location.pathname.split("/").at(-1),
      user: [],
      post: [],
      likes: [],
      comments: [],
      commentForm: {
          post_id: null,
          body: '',
          commenter: null,
      }
    }
    },
    mounted() {
      this.getUser();
      this.getPost();
      this.getComment();
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
        });
      },
      getPost() {
        CustomFetch('http://localhost:8080/posts/'+this.view_post, {
          method: 'GET',
          mode: 'cors',
        })
        .then((res) => {
          this.post = res;
        })
        .catch((error) => {
          console.error(error);
        });
      },
      getComment() {
        CustomFetch('http://localhost:8080/comment/'+this.view_post, {
          method: 'GET',
          mode: 'cors',
        })
        .then((res) => {
          this.comments = res;
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
    goHome() {
      this.$router.push({path:'/dashboard'})
    },
    initForm() {
      this.new_comment='';
    },
    onSubmit() {
      const payload = {
          commenter: this.user.username,
          body: this.new_comment,
        };
        this.addComment(payload);
        this.initForm();
    },
    addComment(new_comment) {
      if(!this.new_comment == "") {
        CustomFetch('http://localhost:8080/comment/'+this.view_post, {
              method: 'POST',
              body: JSON.stringify(new_comment),
              mode: 'cors',
              headers: {
                  'Content-Type': 'application/json',
              },
          })
      .then(() => {
        this.getUser();
        this.getPost();
        this.getComment();
      })
      .catch((error) => {
        console.log(error);
        this.getUser();
        this.getPost();
        this.getComment();
      });
      }
    },
    goEdit() {
      this.$router.push({path:'/profilesettings'})
    },
    deleteComment(comment_id) {
      CustomFetch(`http://localhost:8080/comment/${comment_id}`, {
        method: 'DELETE',
        mode: 'cors',
        headers: {
          'Content-type': 'application/json',
        },
      })
      .then(() => {
        this.$router.go()
      })
      .catch((error) => {
        console.error(error);
        this.$router.go()
      });
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
    } 
  }
</script>

<style>
.post{
background-image: url("../../../static/images/login-back.png");
background-size: cover;
height: 100%;
}
#profile-post{
position: fixed;
font-size: 10px;
top: 15%;
left: 5%;
color: white;
padding: 15px;
box-shadow: 0px 0px 10px rgba(213, 121, 121, 5);
}

#posts{
  padding: 10px;
  margin-top: 6%;
  margin-left: 35%;
}

.card-post{
box-shadow: 0px 0px 10px rgba(2, 2, 2, 0.5);
padding-top: 10px;
padding-left: 10px;
padding-right: 10px;
padding-bottom: 20px;
font-style: oblique;
color: white;
font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
}

</style>
