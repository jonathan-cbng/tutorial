<template>
  <div class="container-fluid border-bottom">
    <!-- DEBUG: CaseDetails rendered for id: {{ id }} -->
    <h3>Case Information</h3>
    <CaseEdit
      v-if="id"
      :id="id"
      @update-success="onCaseUpdated"
      @update-failed="onCaseUpdateFailed"
      @cancel="onCaseEditCancel"
    />
    <CaseEdit
      v-else
      @case-created="onCaseCreated"
      @create-failed="onCaseCreateFailed"
      @cancel="onCaseEditCancel"
    />
  </div>
</template>

<script>
import CaseEdit from './CaseEdit.vue';

export default {
  name: 'CaseDetails',
  props: {
    id: { type: [String, Number], required: false, default: null }
  },
  components: {
    CaseEdit,
  },
  data() {
    return {
    };
  },
  methods: {
    onCaseUpdated() {
      // Optionally, refresh panel list or show a message
    },
    onCaseUpdateFailed(e) {
      // Optionally, handle update failure
    },
    onCaseEditCancel() {
      this.$router.push({ name: 'CaseList' });
    },
    onCaseCreated(newCase) {
      // After creating, navigate to the new case's details
      if (newCase && newCase.id) {
        this.$router.replace({ name: 'CaseDetails', params: { id: newCase.id } });
      } else {
        // fallback: go back to list
        this.$router.push({ name: 'CaseList' });
      }
    },
    onCaseCreateFailed(e) {
      // Optionally, handle create failure
    }
  }
};
</script>

<style scoped>
.asteriskField { color: red; }
</style>
