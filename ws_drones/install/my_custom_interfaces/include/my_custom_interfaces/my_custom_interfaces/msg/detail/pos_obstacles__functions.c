// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from my_custom_interfaces:msg/PosObstacles.idl
// generated code does not contain a copyright notice
#include "my_custom_interfaces/msg/detail/pos_obstacles__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `fixes`
// Member `flotants`
#include "geometry_msgs/msg/detail/point__functions.h"

bool
my_custom_interfaces__msg__PosObstacles__init(my_custom_interfaces__msg__PosObstacles * msg)
{
  if (!msg) {
    return false;
  }
  // fixes
  if (!geometry_msgs__msg__Point__Sequence__init(&msg->fixes, 0)) {
    my_custom_interfaces__msg__PosObstacles__fini(msg);
    return false;
  }
  // flotants
  if (!geometry_msgs__msg__Point__Sequence__init(&msg->flotants, 0)) {
    my_custom_interfaces__msg__PosObstacles__fini(msg);
    return false;
  }
  return true;
}

void
my_custom_interfaces__msg__PosObstacles__fini(my_custom_interfaces__msg__PosObstacles * msg)
{
  if (!msg) {
    return;
  }
  // fixes
  geometry_msgs__msg__Point__Sequence__fini(&msg->fixes);
  // flotants
  geometry_msgs__msg__Point__Sequence__fini(&msg->flotants);
}

bool
my_custom_interfaces__msg__PosObstacles__are_equal(const my_custom_interfaces__msg__PosObstacles * lhs, const my_custom_interfaces__msg__PosObstacles * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // fixes
  if (!geometry_msgs__msg__Point__Sequence__are_equal(
      &(lhs->fixes), &(rhs->fixes)))
  {
    return false;
  }
  // flotants
  if (!geometry_msgs__msg__Point__Sequence__are_equal(
      &(lhs->flotants), &(rhs->flotants)))
  {
    return false;
  }
  return true;
}

bool
my_custom_interfaces__msg__PosObstacles__copy(
  const my_custom_interfaces__msg__PosObstacles * input,
  my_custom_interfaces__msg__PosObstacles * output)
{
  if (!input || !output) {
    return false;
  }
  // fixes
  if (!geometry_msgs__msg__Point__Sequence__copy(
      &(input->fixes), &(output->fixes)))
  {
    return false;
  }
  // flotants
  if (!geometry_msgs__msg__Point__Sequence__copy(
      &(input->flotants), &(output->flotants)))
  {
    return false;
  }
  return true;
}

my_custom_interfaces__msg__PosObstacles *
my_custom_interfaces__msg__PosObstacles__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  my_custom_interfaces__msg__PosObstacles * msg = (my_custom_interfaces__msg__PosObstacles *)allocator.allocate(sizeof(my_custom_interfaces__msg__PosObstacles), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(my_custom_interfaces__msg__PosObstacles));
  bool success = my_custom_interfaces__msg__PosObstacles__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
my_custom_interfaces__msg__PosObstacles__destroy(my_custom_interfaces__msg__PosObstacles * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    my_custom_interfaces__msg__PosObstacles__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
my_custom_interfaces__msg__PosObstacles__Sequence__init(my_custom_interfaces__msg__PosObstacles__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  my_custom_interfaces__msg__PosObstacles * data = NULL;

  if (size) {
    data = (my_custom_interfaces__msg__PosObstacles *)allocator.zero_allocate(size, sizeof(my_custom_interfaces__msg__PosObstacles), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = my_custom_interfaces__msg__PosObstacles__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        my_custom_interfaces__msg__PosObstacles__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
my_custom_interfaces__msg__PosObstacles__Sequence__fini(my_custom_interfaces__msg__PosObstacles__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      my_custom_interfaces__msg__PosObstacles__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

my_custom_interfaces__msg__PosObstacles__Sequence *
my_custom_interfaces__msg__PosObstacles__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  my_custom_interfaces__msg__PosObstacles__Sequence * array = (my_custom_interfaces__msg__PosObstacles__Sequence *)allocator.allocate(sizeof(my_custom_interfaces__msg__PosObstacles__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = my_custom_interfaces__msg__PosObstacles__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
my_custom_interfaces__msg__PosObstacles__Sequence__destroy(my_custom_interfaces__msg__PosObstacles__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    my_custom_interfaces__msg__PosObstacles__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
my_custom_interfaces__msg__PosObstacles__Sequence__are_equal(const my_custom_interfaces__msg__PosObstacles__Sequence * lhs, const my_custom_interfaces__msg__PosObstacles__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!my_custom_interfaces__msg__PosObstacles__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
my_custom_interfaces__msg__PosObstacles__Sequence__copy(
  const my_custom_interfaces__msg__PosObstacles__Sequence * input,
  my_custom_interfaces__msg__PosObstacles__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(my_custom_interfaces__msg__PosObstacles);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    my_custom_interfaces__msg__PosObstacles * data =
      (my_custom_interfaces__msg__PosObstacles *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!my_custom_interfaces__msg__PosObstacles__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          my_custom_interfaces__msg__PosObstacles__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!my_custom_interfaces__msg__PosObstacles__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
