<template>
  <!-- Only render the rows, not the table or headers -->
  <tr v-for="caseItem in caseList" :key="caseItem.id" class="case-row" @click="goToCase(caseItem.id)" role="link" tabindex="0" @keydown.enter="goToCase(caseItem.id)" @keydown.space.prevent="goToCase(caseItem.id)">
    <td class="align-middle min-col-action">
      <div class="d-flex flex-column align-items-stretch w-100 gap-1">
        <button
          class="btn btn-sm btn-danger mb-1 d-flex align-items-center justify-content-center"
          @click.stop="onDeleteCase(caseItem.id)"
          title="Delete case"
        >
          <i class="bi bi-trash"></i>
          <span class="visually-hidden">Delete</span>
        </button>
      </div>
    </td>
    <td class="align-middle min-col-wider">
      {{ caseItem.name }}
    </td>
    <td class="align-middle min-col-wider">
      {{ caseItem.owner }}
    </td>
    <td class="align-middle min-col">
      {{ caseItem.breed && caseItem.breed.species ? caseItem.breed.species : '' }}
    </td>
    <td class="align-middle min-col-breed-sex" :style="breedMinWidth">
      {{ caseItem.breed && caseItem.breed.name ? caseItem.breed.name : '' }}
    </td>
    <td class="align-middle min-col-breed-sex" :style="sexMinWidth">
      {{ caseItem.sex }}
    </td>
    <td class="align-middle min-col">
      {{ caseItem.birth_date }}
    </td>
    <td class="align-middle min-col-wide">
      {{ caseItem.practice_animal_id }}
    </td>
    <td class="align-middle min-col-wide">
      {{ caseItem.chip_id }}
    </td>
    <td class="align-middle notes-col">
      {{ caseItem.notes }}
      <span class="float-end text-secondary"><i class="bi bi-chevron-right"></i></span>
    </td>
  </tr>
</template>

<script>
export default {
  name: 'CaseList',
  emits: ['delete-case', 'row-species-change', 'clean-row-handled'],
  props: {
    caseList: { type: Array, required: true },
    breeds: { type: Array, required: true },
    sexes: { type: Array, required: true },
    errors: Object,
    rowErrors: Object,
    speciesList: { type: Array, required: true },
    selectedSpecies: { type: String, required: false, default: '' },
    cleanRowId: { type: Number, required: false, default: null }
  },
  computed: {
    breedMinWidth() {
      if (!this.breeds || this.breeds.length === 0) return '';
      const maxLen = Math.max(...this.breeds.map(b => b.name.length), 'Select breed...'.length);
      return { minWidth: `${maxLen + 4}ch` };
    },
    sexMinWidth() {
      if (!this.sexes || this.sexes.length === 0) return '';
      const maxLen = Math.max(...this.sexes.map(s => s.length), 'Select sex...'.length);
      return { minWidth: `${maxLen + 4}ch` };
    }
  },
  methods: {
    onDeleteCase(id) {
      if (!confirm('Are you sure you want to delete this case?')) return;
      this.$emit('delete-case', id);
    },
    goToCase(id) {
      this.$router.push({ name: 'CaseDetails', params: { id } });
    }
  }
};
</script>

<style scoped>
.table {
  width: 100%;
  table-layout: auto;
}
.min-col {
  min-width: 125px;
}
.min-col-wide {
  min-width: 175px;
}
.min-col-wider {
  min-width: 200px;
}
.min-col-action {
  min-width: 90px;
}
.notes-col {
  width: 100%;
  min-width: 120px;
  max-width: 600px;
  white-space: normal;
  word-break: break-word;
}
.notes-textarea {
  width: 100%;
  min-height: 38px;
  resize: vertical;
  white-space: pre-wrap;
  word-break: break-word;
}
.table-primary {
  background-color: #e9ecef;
}
.table td.align-middle > span {
  line-height: 1.5;
  vertical-align: middle;
}
.case-row {
  cursor: pointer;
}
.case-row:hover, .case-row:focus {
  background-color: #f5f5f5;
  outline: 2px solid #0d6efd;
}
.case-row:active {
  background-color: #e2e6ea;
}
</style>
