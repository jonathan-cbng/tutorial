<template>
  <Layout
    :user="null"
    :deployment-id="deploymentId"
    :deployment-colour="deploymentColour"
    :deployment-name="deploymentName"
    :logo-url="logoUrl"
  >
    <router-view />
  </Layout>
</template>

<script>
import Layout from './components/Layout.vue';

export default {
  name: 'App',
  components: { Layout },
  data() {
    return {
      deploymentId: 'production',
      deploymentColour: '#333',
      deploymentName: '',
    };
  }
};
</script>

<style scoped>
body {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}
</style>
