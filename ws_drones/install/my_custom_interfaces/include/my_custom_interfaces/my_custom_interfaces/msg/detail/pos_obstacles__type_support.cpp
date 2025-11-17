// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from my_custom_interfaces:msg/PosObstacles.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "my_custom_interfaces/msg/detail/pos_obstacles__functions.h"
#include "my_custom_interfaces/msg/detail/pos_obstacles__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace my_custom_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void PosObstacles_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) my_custom_interfaces::msg::PosObstacles(_init);
}

void PosObstacles_fini_function(void * message_memory)
{
  auto typed_message = static_cast<my_custom_interfaces::msg::PosObstacles *>(message_memory);
  typed_message->~PosObstacles();
}

size_t size_function__PosObstacles__fixes(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<geometry_msgs::msg::Point> *>(untyped_member);
  return member->size();
}

const void * get_const_function__PosObstacles__fixes(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<geometry_msgs::msg::Point> *>(untyped_member);
  return &member[index];
}

void * get_function__PosObstacles__fixes(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<geometry_msgs::msg::Point> *>(untyped_member);
  return &member[index];
}

void fetch_function__PosObstacles__fixes(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const geometry_msgs::msg::Point *>(
    get_const_function__PosObstacles__fixes(untyped_member, index));
  auto & value = *reinterpret_cast<geometry_msgs::msg::Point *>(untyped_value);
  value = item;
}

void assign_function__PosObstacles__fixes(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<geometry_msgs::msg::Point *>(
    get_function__PosObstacles__fixes(untyped_member, index));
  const auto & value = *reinterpret_cast<const geometry_msgs::msg::Point *>(untyped_value);
  item = value;
}

void resize_function__PosObstacles__fixes(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<geometry_msgs::msg::Point> *>(untyped_member);
  member->resize(size);
}

size_t size_function__PosObstacles__flotants(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<geometry_msgs::msg::Point> *>(untyped_member);
  return member->size();
}

const void * get_const_function__PosObstacles__flotants(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<geometry_msgs::msg::Point> *>(untyped_member);
  return &member[index];
}

void * get_function__PosObstacles__flotants(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<geometry_msgs::msg::Point> *>(untyped_member);
  return &member[index];
}

void fetch_function__PosObstacles__flotants(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const geometry_msgs::msg::Point *>(
    get_const_function__PosObstacles__flotants(untyped_member, index));
  auto & value = *reinterpret_cast<geometry_msgs::msg::Point *>(untyped_value);
  value = item;
}

void assign_function__PosObstacles__flotants(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<geometry_msgs::msg::Point *>(
    get_function__PosObstacles__flotants(untyped_member, index));
  const auto & value = *reinterpret_cast<const geometry_msgs::msg::Point *>(untyped_value);
  item = value;
}

void resize_function__PosObstacles__flotants(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<geometry_msgs::msg::Point> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember PosObstacles_message_member_array[2] = {
  {
    "fixes",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Point>(),  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(my_custom_interfaces::msg::PosObstacles, fixes),  // bytes offset in struct
    nullptr,  // default value
    size_function__PosObstacles__fixes,  // size() function pointer
    get_const_function__PosObstacles__fixes,  // get_const(index) function pointer
    get_function__PosObstacles__fixes,  // get(index) function pointer
    fetch_function__PosObstacles__fixes,  // fetch(index, &value) function pointer
    assign_function__PosObstacles__fixes,  // assign(index, value) function pointer
    resize_function__PosObstacles__fixes  // resize(index) function pointer
  },
  {
    "flotants",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Point>(),  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(my_custom_interfaces::msg::PosObstacles, flotants),  // bytes offset in struct
    nullptr,  // default value
    size_function__PosObstacles__flotants,  // size() function pointer
    get_const_function__PosObstacles__flotants,  // get_const(index) function pointer
    get_function__PosObstacles__flotants,  // get(index) function pointer
    fetch_function__PosObstacles__flotants,  // fetch(index, &value) function pointer
    assign_function__PosObstacles__flotants,  // assign(index, value) function pointer
    resize_function__PosObstacles__flotants  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers PosObstacles_message_members = {
  "my_custom_interfaces::msg",  // message namespace
  "PosObstacles",  // message name
  2,  // number of fields
  sizeof(my_custom_interfaces::msg::PosObstacles),
  false,  // has_any_key_member_
  PosObstacles_message_member_array,  // message members
  PosObstacles_init_function,  // function to initialize message memory (memory has to be allocated)
  PosObstacles_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t PosObstacles_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &PosObstacles_message_members,
  get_message_typesupport_handle_function,
  &my_custom_interfaces__msg__PosObstacles__get_type_hash,
  &my_custom_interfaces__msg__PosObstacles__get_type_description,
  &my_custom_interfaces__msg__PosObstacles__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace my_custom_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<my_custom_interfaces::msg::PosObstacles>()
{
  return &::my_custom_interfaces::msg::rosidl_typesupport_introspection_cpp::PosObstacles_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, my_custom_interfaces, msg, PosObstacles)() {
  return &::my_custom_interfaces::msg::rosidl_typesupport_introspection_cpp::PosObstacles_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
