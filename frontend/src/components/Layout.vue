<template>
  <div>
    <!-- Deployment banner -->
    <nav v-if="deploymentId !== 'production'" class="navbar navbar-expand-sm sticky-top navbar-dark" :style="{ backgroundColor: deploymentColour }">
      <div class="navbar-text"></div>
      <div class="navbar-text navbar-nav navbar-center navbar-brand">
        {{ deploymentName }}
      </div>
    </nav>
    <!-- Main navbar -->
    <nav class="navbar navbar-expand-sm bg-primary navbar-dark sticky-top">
      <router-link class="navbar-brand" to="/cases">
        Tutorial
      </router-link>
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link class="nav-link" active-class="active" to="/cases">
            Cases
          </router-link>
        </li>
      </ul>
    </nav>
    <!-- Add margin below navbars to prevent overlap with content -->
    <div style="height: 1rem;"></div>
    <div class="container-fluid">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Layout',
  props: {
    user: Object,
    section: String,
    deploymentId: {
      type: String,
      default: 'production'
    },
    deploymentColour: {
      type: String,
      default: '#333'
    },
    deploymentName: {
      type: String,
      default: ''
    }
  }
};
</script>

<style scoped>
.navbar-center {
  margin: 0 auto;
}
</style>
