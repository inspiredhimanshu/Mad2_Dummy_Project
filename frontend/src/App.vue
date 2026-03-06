<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
    <div class="container">

  <nav class="navbar navbar-expand-lg navbar-light bg-light">

    <RouterLink class="navbar-brand" to="/">Grocery Store</RouterLink>

    <button 
      class="navbar-toggler" 
      type="button" 
      data-bs-toggle="collapse" 
      data-bs-target="#navbarSupportedContent"
      aria-controls="navbarSupportedContent" 
      aria-expanded="false" 
      aria-label="Toggle navigation">

      <span class="navbar-toggler-icon"></span>
    </button>


    <div class="collapse navbar-collapse" id="navbarSupportedContent">

      <!-- Search Bar -->
      <form class="d-flex mx-auto">
        <input 
          class="form-control me-2" 
          type="search" 
          placeholder="Search products..."
        >
        <button class="btn btn-outline-success" type="submit">
          Search
        </button>
      </form>

      <!-- Right side menu -->
      <ul class="navbar-nav ms-auto">

        <li class="nav-item">
          <RouterLink class="nav-link" to="/login">
            Login
          </RouterLink>
        </li>

      </ul>

    </div>

  </nav>

  <RouterView/>

</div>

</template>

