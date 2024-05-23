<template>
    <h1>
        {{ msg }}
    </h1>
    <button @click="$emit('update:msg', 'Hello Vue 3!')">
        Emit Event
    </button>
</template>
<script>
export default {
  name: 'MyCompoent',
  props: {
    msg: String
  },
  methods: {
    submit() {
      this.$emit('someEvent')
    }
  },
}
</script>