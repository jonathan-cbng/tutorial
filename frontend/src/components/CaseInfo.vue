<template>
  <div class="case-info-simple">
    <div class="case-field"><strong>Name</strong> {{ caseData.name }}</div>
    <div class="case-field"><strong>Owner</strong> {{ caseData.owner }}</div>
    <div class="case-field"><strong>Species</strong> {{ caseData.breed && caseData.breed.species ? caseData.breed.species : '' }}</div>
    <div class="case-field"><strong>Breed</strong> {{ caseData.breed && caseData.breed.name ? caseData.breed.name : '' }}</div>
    <div class="case-field"><strong>Sex</strong> {{ caseData.sex }}</div>
    <div class="case-field"><strong>Birthdate</strong> {{ caseData.birth_date }}</div>
    <div class="case-field"><strong>Practice Animal ID</strong> {{ caseData.practice_animal_id }}</div>
    <div class="case-field"><strong>Chip ID</strong> {{ caseData.chip_id }}</div>
    <div class="case-field"><strong>Notes</strong> <span style="white-space: pre-line">{{ caseData.notes }}</span></div>
  </div>
</template>

<script>
export default {
  name: 'CaseInfo',
  props: {
    caseData: {
      type: Object,
      required: true
    }
  }
};
</script>

<style scoped>
.case-info-simple {
  max-width: 700px;
  margin: 0 auto 2rem auto;
  padding: 1rem 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}
.case-field {
  margin-bottom: 0.5rem;
  font-size: 1rem;
}
.case-field strong {
  min-width: 160px;
  display: inline-block;
}
</style>
