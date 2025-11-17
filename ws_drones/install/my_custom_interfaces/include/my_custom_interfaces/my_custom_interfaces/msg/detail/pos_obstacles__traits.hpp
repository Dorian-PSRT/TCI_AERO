// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from my_custom_interfaces:msg/PosObstacles.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "my_custom_interfaces/msg/pos_obstacles.hpp"


#ifndef MY_CUSTOM_INTERFACES__MSG__DETAIL__POS_OBSTACLES__TRAITS_HPP_
#define MY_CUSTOM_INTERFACES__MSG__DETAIL__POS_OBSTACLES__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "my_custom_interfaces/msg/detail/pos_obstacles__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'fixes'
// Member 'flotants'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace my_custom_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const PosObstacles & msg,
  std::ostream & out)
{
  out << "{";
  // member: fixes
  {
    if (msg.fixes.size() == 0) {
      out << "fixes: []";
    } else {
      out << "fixes: [";
      size_t pending_items = msg.fixes.size();
      for (auto item : msg.fixes) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: flotants
  {
    if (msg.flotants.size() == 0) {
      out << "flotants: []";
    } else {
      out << "flotants: [";
      size_t pending_items = msg.flotants.size();
      for (auto item : msg.flotants) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PosObstacles & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: fixes
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.fixes.size() == 0) {
      out << "fixes: []\n";
    } else {
      out << "fixes:\n";
      for (auto item : msg.fixes) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: flotants
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.flotants.size() == 0) {
      out << "flotants: []\n";
    } else {
      out << "flotants:\n";
      for (auto item : msg.flotants) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PosObstacles & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace my_custom_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use my_custom_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const my_custom_interfaces::msg::PosObstacles & msg,
  std::ostream & out, size_t indentation = 0)
{
  my_custom_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use my_custom_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const my_custom_interfaces::msg::PosObstacles & msg)
{
  return my_custom_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<my_custom_interfaces::msg::PosObstacles>()
{
  return "my_custom_interfaces::msg::PosObstacles";
}

template<>
inline const char * name<my_custom_interfaces::msg::PosObstacles>()
{
  return "my_custom_interfaces/msg/PosObstacles";
}

template<>
struct has_fixed_size<my_custom_interfaces::msg::PosObstacles>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<my_custom_interfaces::msg::PosObstacles>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<my_custom_interfaces::msg::PosObstacles>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MY_CUSTOM_INTERFACES__MSG__DETAIL__POS_OBSTACLES__TRAITS_HPP_
