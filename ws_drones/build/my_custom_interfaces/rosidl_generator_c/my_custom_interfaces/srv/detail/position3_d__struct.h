// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from my_custom_interfaces:srv/Position3D.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "my_custom_interfaces/srv/position3_d.h"


#ifndef MY_CUSTOM_INTERFACES__SRV__DETAIL__POSITION3_D__STRUCT_H_
#define MY_CUSTOM_INTERFACES__SRV__DETAIL__POSITION3_D__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'point'
#include "geometry_msgs/msg/detail/point__struct.h"

/// Struct defined in srv/Position3D in the package my_custom_interfaces.
typedef struct my_custom_interfaces__srv__Position3D_Request
{
  geometry_msgs__msg__Point point;
} my_custom_interfaces__srv__Position3D_Request;

// Struct for a sequence of my_custom_interfaces__srv__Position3D_Request.
typedef struct my_custom_interfaces__srv__Position3D_Request__Sequence
{
  my_custom_interfaces__srv__Position3D_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_custom_interfaces__srv__Position3D_Request__Sequence;

// Constants defined in the message

/// Struct defined in srv/Position3D in the package my_custom_interfaces.
typedef struct my_custom_interfaces__srv__Position3D_Response
{
  bool success;
} my_custom_interfaces__srv__Position3D_Response;

// Struct for a sequence of my_custom_interfaces__srv__Position3D_Response.
typedef struct my_custom_interfaces__srv__Position3D_Response__Sequence
{
  my_custom_interfaces__srv__Position3D_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_custom_interfaces__srv__Position3D_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  my_custom_interfaces__srv__Position3D_Event__request__MAX_SIZE = 1
};
// response
enum
{
  my_custom_interfaces__srv__Position3D_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/Position3D in the package my_custom_interfaces.
typedef struct my_custom_interfaces__srv__Position3D_Event
{
  service_msgs__msg__ServiceEventInfo info;
  my_custom_interfaces__srv__Position3D_Request__Sequence request;
  my_custom_interfaces__srv__Position3D_Response__Sequence response;
} my_custom_interfaces__srv__Position3D_Event;

// Struct for a sequence of my_custom_interfaces__srv__Position3D_Event.
typedef struct my_custom_interfaces__srv__Position3D_Event__Sequence
{
  my_custom_interfaces__srv__Position3D_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_custom_interfaces__srv__Position3D_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MY_CUSTOM_INTERFACES__SRV__DETAIL__POSITION3_D__STRUCT_H_
