<template>
  <form @submit.prevent="onSubmit">
    <fieldset>
      <div class="row">
        <!-- Column 1: Name, Owner, Notes -->
        <div class="col-sm-4">
          <div class="form-group mb-3" id="div_id_name">
            <div class="row align-items-center">
              <label for="id_name" class="col-3 col-form-label requiredField">
                Name<span class="asteriskField">*</span>
              </label>
              <div class="col-9">
                <input type="text" v-model="form.name" maxlength="200" class="form-control" required id="id_name">
              </div>
            </div>
          </div>
          <div class="form-group mb-3" id="div_id_owner">
            <div class="row align-items-center">
              <label for="id_owner" class="col-3 col-form-label requiredField">
                Owner<span class="asteriskField">*</span>
              </label>
              <div class="col-9">
                <input type="text" v-model="form.owner" maxlength="200" class="form-control" required id="id_owner">
              </div>
            </div>
          </div>
          <div class="form-group mb-3" id="div_id_notes">
            <div class="row align-items-center">
              <label for="id_notes" class="col-3 col-form-label">
                Notes
              </label>
              <div class="col-9">
                <textarea v-model="form.notes" cols="40" rows="3" class="form-control" id="id_notes"></textarea>
              </div>
            </div>
          </div>
        </div>
        <!-- Column 2: Species, Breed, Sex -->
        <div class="col-sm-4">
          <div class="form-group mb-3" id="div_id_species">
            <div class="row align-items-center">
              <label for="id_species" class="col-3 col-form-label requiredField">
                Species<span class="asteriskField">*</span>
              </label>
              <div class="col-9">
                <select v-model="form.species" class="form-select" id="id_species" required @change="onSpeciesChange">
                  <option value="">---------</option>
                  <option v-for="species in speciesList" :key="species" :value="species">{{ species }}</option>
                </select>
              </div>
            </div>
          </div>
          <div class="form-group mb-3" id="div_id_breed">
            <div class="row align-items-center">
              <label for="id_breed" class="col-3 col-form-label requiredField">
                Breed<span class="asteriskField">*</span>
              </label>
              <div class="col-9">
                <select v-model="form.breed_id" class="form-select" required id="id_breed">
                  <option value="">---------</option>
                  <option v-for="breed in filteredBreeds()" :key="breed.id" :value="breed.id">{{ breed.name }}</option>
                </select>
              </div>
            </div>
          </div>
          <div class="form-group mb-3" id="div_id_sex">
            <div class="row align-items-center">
              <label for="id_sex" class="col-3 col-form-label requiredField">
                Sex<span class="asteriskField">*</span>
              </label>
              <div class="col-9">
                <select v-model="form.sex" class="form-select" required id="id_sex">
                  <option value="">---------</option>
                  <option v-for="sex in sexes" :key="sex" :value="sex">{{ sex }}</option>
                </select>
              </div>
            </div>
          </div>
        </div>
        <!-- Column 3: Birthdate, Chip ID, Practice Animal ID, Update Button -->
        <div class="col-sm-4">
          <div class="form-group mb-3" id="div_id_birth_date">
            <div class="row align-items-center">
              <label for="id_birth_date" class="col-3 col-form-label requiredField">
                Birthdate<span class="asteriskField">*</span>
              </label>
              <div class="col-9">
                <input type="date" v-model="form.birth_date" class="form-control" required id="id_birth_date">
              </div>
            </div>
          </div>
          <div class="form-group mb-3" id="div_id_chip_id">
            <div class="row align-items-center">
              <label for="id_chip_id" class="col-3 col-form-label">
                Chip id
              </label>
              <div class="col-9">
                <input type="text" v-model="form.chip_id" maxlength="32" class="form-control" id="id_chip_id">
              </div>
            </div>
          </div>
          <div class="form-group mb-3" id="div_id_practice_animal_id">
            <div class="row align-items-center">
              <label for="id_practice_animal_id" class="col-3 col-form-label">
                Practice animal id
              </label>
              <div class="col-9">
                <input type="text" v-model="form.practice_animal_id" maxlength="50" class="form-control" id="id_practice_animal_id">
              </div>
            </div>
          </div>
          <div class="form-group mb-3">
            <div class="row align-items-center">
              <div class="col-12 text-end">
                <input v-if="isDirty" type="submit" value="Save" class="btn btn-primary me-2" id="submit-id-save">
                <button v-if="isDirty" type="button" class="btn btn-outline-secondary me-2" @click="onCancel">Cancel</button>
                <button type="button" class="btn btn-secondary" @click="onBack">Back</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </fieldset>
  </form>
</template>

<script>
import { fetchCase, updateCase, addCase, fetchBreeds, fetchSexes, fetchSpecies } from '../api.js';
import { useApiErrorHandler } from '../api.js';

export default {
  name: 'CaseEdit',
  props: {
    id: { type: [String, Number], required: false, default: null }
  },
  setup() {
    const { showPopup, popupMessage, handleError, closePopup } = useApiErrorHandler();
    return { showPopup, popupMessage, handleError, closePopup };
  },
  data() {
    const initialForm = {
      name: '',
      owner: '',
      notes: '',
      birth_date: '',
      breed_id: '',
      sex: '',
      chip_id: '',
      practice_animal_id: ''
    };
    return {
      form: { ...initialForm },
      originalForm: { ...initialForm },
      breeds: [],
      speciesList: [],
      sexes: [],
      updateSuccess: false
    };
  },
  computed: {
    isDirty() {
      if (!this.originalForm) return false;
      return Object.keys(this.form).some(
        key => this.form[key] !== this.originalForm[key]
      );
    }
  },
  created() {
    this.loadData();
  },
  methods: {
    async loadData() {
      const promises = [
        this.fetchBreeds(),
        this.fetchSexes(),
        this.fetchSpeciesList()
      ];
      if (this.id) {
        promises.unshift(this.fetchCase());
      } else {
        // If creating, ensure form is empty
        this.form = {
          name: '',
          owner: '',
          notes: '',
          birth_date: '',
          species: '',
          breed_id: '',
          sex: '',
          chip_id: '',
          practice_animal_id: ''
        };
        this.originalForm = { ...this.form };
      }
      await Promise.all(promises);
    },
    async fetchCase() {
      try {
        const data = await fetchCase(this.id);
        this.form = {
          name: data.name || '',
          owner: data.owner || '',
          notes: data.notes || '',
          birth_date: data.birth_date || '',
          species: data.breed?.species || '',
          breed_id: data.breed?.id || '',
          sex: data.sex || '',
          chip_id: data.chip_id || '',
          practice_animal_id: data.practice_animal_id || ''
        };
        this.originalForm = { ...this.form };
      } catch (e) {
        this.handleError(e, 'Failed to fetch case details.');
        this.$emit('update-failed', e);
      }
    },
    async fetchBreeds() {
      try {
        this.breeds = await fetchBreeds();
      } catch (e) {
        this.handleError(e, 'Failed to fetch breeds.');
      }
    },
    async fetchSexes() {
      try {
        this.sexes = await fetchSexes();
      } catch (e) {
        this.handleError(e, 'Failed to fetch sexes.');
      }
    },
    async fetchSpeciesList() {
      try {
        this.speciesList = await fetchSpecies();
      } catch (e) {
        this.handleError(e, 'Failed to fetch species.');
      }
    },
    filteredBreeds() {
      if (!this.form.species) return this.breeds;
      return this.breeds.filter(b => b.species === this.form.species);
    },
    async onSubmit() {
      this.updateSuccess = false;
      try {
        if (this.id) {
          await updateCase(this.id, this.form);
          this.originalForm = { ...this.form };
          this.updateSuccess = true;
          // Navigate to case list after successful update
          this.$router.push({ name: 'CaseList' });
        } else {
          // Create new case
          const newCase = await addCase(this.form);
          this.originalForm = { ...this.form };
          this.updateSuccess = true;
          // Navigate to case list after successful creation
          this.$router.push({ name: 'CaseList' });
        }
      } catch (e) {
        this.handleError(e, this.id ? 'Failed to update case.' : 'Failed to create case.');
        this.$emit(this.id ? 'update-failed' : 'create-failed', e);
      }
    },
    onBack() {
      this.$emit('cancel');
    },
    onCancel() {
      this.form = { ...this.originalForm };
      this.$emit('cancel');
    },
    onSpeciesChange() {
      // Reset breed_id if the species changes
      this.form.breed_id = '';
    }
  }
};
</script>

<style scoped>
.asteriskField { color: red; }
</style>
