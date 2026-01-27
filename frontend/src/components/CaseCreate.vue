<template>
  <tr class="table-primary">
    <td class="align-middle min-col-action">
      <button class="btn btn-success mb-1 w-100 d-flex align-items-center justify-content-center" type="button" @click="onAddCase" title="Create">
        <i class="bi bi-plus-circle me-1"></i>
        <span class="visually-hidden">Create</span>
      </button>
    </td>
    <td class="align-middle min-col-wider">
      <input v-model="form.name" class="form-control" placeholder="Name" />
      <span class="text-danger">{{ errors.name }}</span>
    </td>
    <td class="align-middle min-col-wider">
      <input v-model="form.owner" class="form-control" placeholder="Owner" />
      <span class="text-danger">{{ errors.owner }}</span>
    </td>
    <td class="align-middle min-col">
      <select v-model="form.species" class="form-control" @change="onSpeciesChangeForm" required>
        <option disabled value="">Select species...</option>
        <option v-for="species in speciesList" :key="species" :value="species">{{ species }}</option>
      </select>
      <span class="text-danger">{{ errors.species }}</span>
    </td>
    <td class="align-middle min-col-breed-sex" :style="breedMinWidth">
      <select v-model="form.breed_id" class="form-control">
        <option disabled value="">Select breed...</option>
        <option v-for="breed in breeds" :key="breed.id" :value="breed.id">{{ breed.name }}</option>
      </select>
      <span class="text-danger">{{ errors.breed_id }}</span>
    </td>
    <td class="align-middle min-col-breed-sex" :style="sexMinWidth">
      <select v-model="form.sex" class="form-control">
        <option disabled value="">Select sex...</option>
        <option v-for="sex in sexes" :key="sex" :value="sex">{{ sex }}</option>
      </select>
      <span class="text-danger">{{ errors.sex }}</span>
    </td>
    <td class="align-middle min-col">
      <input v-model="form.birth_date" type="date" class="form-control" :max="today" />
      <span class="text-danger">{{ errors.birth_date }}</span>
    </td>
    <td class="align-middle min-col-wide">
      <input v-model="form.practice_animal_id" class="form-control" placeholder="Practice Animal ID" />
      <span class="text-danger">{{ errors.practice_animal_id }}</span>
    </td>
    <td class="align-middle min-col-wide">
      <input v-model="form.chip_id" class="form-control" placeholder="Chip ID" />
      <span class="text-danger">{{ errors.chip_id }}</span>
    </td>
    <td class="align-middle notes-col">
      <textarea v-model="form.notes" class="form-control notes-textarea" placeholder="Notes"></textarea>
      <span class="text-danger">{{ errors.notes }}</span>
    </td>
  </tr>
</template>

<script>
export default {
  name: 'CaseCreate',
  props: {
    speciesList: { type: Array, required: true },
    breeds: { type: Array, required: true },
    sexes: { type: Array, required: true },
    errors: { type: Object, default: () => ({}) },
    selectedSpecies: { type: String, default: '' },
    breedMinWidth: { type: Object, default: () => ({}) },
    sexMinWidth: { type: Object, default: () => ({}) }
  },
  data() {
    return {
      form: {
        name: '',
        owner: '',
        species: this.selectedSpecies || '',
        breed_id: this.breeds.length ? this.breeds[0].id : '',
        sex: '',
        birth_date: '',
        practice_animal_id: '',
        chip_id: '',
        notes: ''
      },
      today: new Date().toISOString().slice(0, 10)
    };
  },
  watch: {
    selectedSpecies(newVal) {
      if (newVal !== this.form.species) {
        this.form.species = newVal;
        this.form.breed_id = this.breeds.length ? this.breeds[0].id : '';
      }
    },
    breeds(newBreeds) {
      if (!newBreeds.find(b => b.id === this.form.breed_id)) {
        this.form.breed_id = '';
      }
    }
  },
  methods: {
    onSpeciesChangeForm(e) {
      this.$emit('species-change', e.target.value);
      this.form.breed_id = '';
    },
    validateCase(caseObj) {
      const errors = {};
      if (!caseObj.name || !caseObj.name.trim()) errors.name = 'Name is required.';
      if (!caseObj.species) errors.species = 'Species is required.';
      if (!caseObj.breed_id) errors.breed_id = 'Breed is required.';
      if (!caseObj.sex) errors.sex = 'Sex is required.';
      if (!caseObj.birth_date) errors.birth_date = 'Birth date is required.';
      return errors;
    },
    onAddCase() {
      const errors = this.validateCase(this.form);
      if (Object.keys(errors).length > 0) {
        this.$emit('update:errors', errors);
        return;
      }
      this.$emit('add-case', { ...this.form });
      this.form = {
        name: '',
        owner: '',
        species: this.selectedSpecies || '',
        breed_id: this.breeds.length ? this.breeds[0].id : '',
        sex: '',
        birth_date: '',
        practice_animal_id: '',
        chip_id: '',
        notes: ''
      };
      this.$emit('update:errors', {});
    }
  }
};
</script>
