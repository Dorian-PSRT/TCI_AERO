// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from my_custom_interfaces:msg/PosObstacles.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "my_custom_interfaces/msg/detail/pos_obstacles__rosidl_typesupport_introspection_c.h"
#include "my_custom_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "my_custom_interfaces/msg/detail/pos_obstacles__functions.h"
#include "my_custom_interfaces/msg/detail/pos_obstacles__struct.h"


// Include directives for member types
// Member `fixes`
// Member `flotants`
#include "geometry_msgs/msg/point.h"
// Member `fixes`
// Member `flotants`
#include "geometry_msgs/msg/detail/point__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__PosObstacles_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  my_custom_interfaces__msg__PosObstacles__init(message_memory);
}

void my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__PosObstacles_fini_function(void * message_memory)
{
  my_custom_interfaces__msg__PosObstacles__fini(message_memory);
}

size_t my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__size_function__PosObstacles__fixes(
  const void * untyped_member)
{
  const geometry_msgs__msg__Point__Sequence * member =
    (const geometry_msgs__msg__Point__Sequence *)(untyped_member);
  return member->size;
}

const void * my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__get_const_function__PosObstacles__fixes(
  const void * untyped_member, size_t index)
{
  const geometry_msgs__msg__Point__Sequence * member =
    (const geometry_msgs__msg__Point__Sequence *)(untyped_member);
  return &member->data[index];
}

void * my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__get_function__PosObstacles__fixes(
  void * untyped_member, size_t index)
{
  geometry_msgs__msg__Point__Sequence * member =
    (geometry_msgs__msg__Point__Sequence *)(untyped_member);
  return &member->data[index];
}

void my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__fetch_function__PosObstacles__fixes(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const geometry_msgs__msg__Point * item =
    ((const geometry_msgs__msg__Point *)
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__get_const_function__PosObstacles__fixes(untyped_member, index));
  geometry_msgs__msg__Point * value =
    (geometry_msgs__msg__Point *)(untyped_value);
  *value = *item;
}

void my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__assign_function__PosObstacles__fixes(
  void * untyped_member, size_t index, const void * untyped_value)
{
  geometry_msgs__msg__Point * item =
    ((geometry_msgs__msg__Point *)
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__get_function__PosObstacles__fixes(untyped_member, index));
  const geometry_msgs__msg__Point * value =
    (const geometry_msgs__msg__Point *)(untyped_value);
  *item = *value;
}

bool my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__resize_function__PosObstacles__fixes(
  void * untyped_member, size_t size)
{
  geometry_msgs__msg__Point__Sequence * member =
    (geometry_msgs__msg__Point__Sequence *)(untyped_member);
  geometry_msgs__msg__Point__Sequence__fini(member);
  return geometry_msgs__msg__Point__Sequence__init(member, size);
}

size_t my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__size_function__PosObstacles__flotants(
  const void * untyped_member)
{
  const geometry_msgs__msg__Point__Sequence * member =
    (const geometry_msgs__msg__Point__Sequence *)(untyped_member);
  return member->size;
}

const void * my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__get_const_function__PosObstacles__flotants(
  const void * untyped_member, size_t index)
{
  const geometry_msgs__msg__Point__Sequence * member =
    (const geometry_msgs__msg__Point__Sequence *)(untyped_member);
  return &member->data[index];
}

void * my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__get_function__PosObstacles__flotants(
  void * untyped_member, size_t index)
{
  geometry_msgs__msg__Point__Sequence * member =
    (geometry_msgs__msg__Point__Sequence *)(untyped_member);
  return &member->data[index];
}

void my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__fetch_function__PosObstacles__flotants(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const geometry_msgs__msg__Point * item =
    ((const geometry_msgs__msg__Point *)
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__get_const_function__PosObstacles__flotants(untyped_member, index));
  geometry_msgs__msg__Point * value =
    (geometry_msgs__msg__Point *)(untyped_value);
  *value = *item;
}

void my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__assign_function__PosObstacles__flotants(
  void * untyped_member, size_t index, const void * untyped_value)
{
  geometry_msgs__msg__Point * item =
    ((geometry_msgs__msg__Point *)
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__get_function__PosObstacles__flotants(untyped_member, index));
  const geometry_msgs__msg__Point * value =
    (const geometry_msgs__msg__Point *)(untyped_value);
  *item = *value;
}

bool my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__resize_function__PosObstacles__flotants(
  void * untyped_member, size_t size)
{
  geometry_msgs__msg__Point__Sequence * member =
    (geometry_msgs__msg__Point__Sequence *)(untyped_member);
  geometry_msgs__msg__Point__Sequence__fini(member);
  return geometry_msgs__msg__Point__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__PosObstacles_message_member_array[2] = {
  {
    "fixes",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(my_custom_interfaces__msg__PosObstacles, fixes),  // bytes offset in struct
    NULL,  // default value
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__size_function__PosObstacles__fixes,  // size() function pointer
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__get_const_function__PosObstacles__fixes,  // get_const(index) function pointer
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__get_function__PosObstacles__fixes,  // get(index) function pointer
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__fetch_function__PosObstacles__fixes,  // fetch(index, &value) function pointer
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__assign_function__PosObstacles__fixes,  // assign(index, value) function pointer
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__resize_function__PosObstacles__fixes  // resize(index) function pointer
  },
  {
    "flotants",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(my_custom_interfaces__msg__PosObstacles, flotants),  // bytes offset in struct
    NULL,  // default value
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__size_function__PosObstacles__flotants,  // size() function pointer
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__get_const_function__PosObstacles__flotants,  // get_const(index) function pointer
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__get_function__PosObstacles__flotants,  // get(index) function pointer
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__fetch_function__PosObstacles__flotants,  // fetch(index, &value) function pointer
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__assign_function__PosObstacles__flotants,  // assign(index, value) function pointer
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__resize_function__PosObstacles__flotants  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__PosObstacles_message_members = {
  "my_custom_interfaces__msg",  // message namespace
  "PosObstacles",  // message name
  2,  // number of fields
  sizeof(my_custom_interfaces__msg__PosObstacles),
  false,  // has_any_key_member_
  my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__PosObstacles_message_member_array,  // message members
  my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__PosObstacles_init_function,  // function to initialize message memory (memory has to be allocated)
  my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__PosObstacles_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__PosObstacles_message_type_support_handle = {
  0,
  &my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__PosObstacles_message_members,
  get_message_typesupport_handle_function,
  &my_custom_interfaces__msg__PosObstacles__get_type_hash,
  &my_custom_interfaces__msg__PosObstacles__get_type_description,
  &my_custom_interfaces__msg__PosObstacles__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_my_custom_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, my_custom_interfaces, msg, PosObstacles)() {
  my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__PosObstacles_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Point)();
  my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__PosObstacles_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Point)();
  if (!my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__PosObstacles_message_type_support_handle.typesupport_identifier) {
    my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__PosObstacles_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &my_custom_interfaces__msg__PosObstacles__rosidl_typesupport_introspection_c__PosObstacles_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
