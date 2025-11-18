// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from my_custom_interfaces:msg/PosObstacles.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "my_custom_interfaces/msg/pos_obstacles.h"


#ifndef MY_CUSTOM_INTERFACES__MSG__DETAIL__POS_OBSTACLES__STRUCT_H_
#define MY_CUSTOM_INTERFACES__MSG__DETAIL__POS_OBSTACLES__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'fixes'
// Member 'flotants'
#include "geometry_msgs/msg/detail/point__struct.h"

/// Struct defined in msg/PosObstacles in the package my_custom_interfaces.
typedef struct my_custom_interfaces__msg__PosObstacles
{
  geometry_msgs__msg__Point__Sequence fixes;
  geometry_msgs__msg__Point__Sequence flotants;
} my_custom_interfaces__msg__PosObstacles;

// Struct for a sequence of my_custom_interfaces__msg__PosObstacles.
typedef struct my_custom_interfaces__msg__PosObstacles__Sequence
{
  my_custom_interfaces__msg__PosObstacles * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_custom_interfaces__msg__PosObstacles__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MY_CUSTOM_INTERFACES__MSG__DETAIL__POS_OBSTACLES__STRUCT_H_
