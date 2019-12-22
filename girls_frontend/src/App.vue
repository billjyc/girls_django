<template>
  <v-app id="inspire">
    <navigation
      :drawer="drawer"
      :mini-variant="miniVariant"
    />
    <toolbar
      :title="title"
      @toolbarSideIconClicked="showNavigation"
    />
    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script>
  import Navigation from '@/components/Navigation'
  import Toolbar from '@/components/Toolbar'
  export default {
    components: {
      Navigation,
      Toolbar,
    },
    props: {
      source: String,
    },
    data: () => ({
      dialog: false,
      drawer: true,
      miniVariant: false,
      title: 'SNH48 Data',
    }),
    methods: {
      showNavigation () {
        this.drawer = !this.drawer
      },
    },
  }
</script>
