// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_custom_interfaces:msg/PosObstacles.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "my_custom_interfaces/msg/pos_obstacles.hpp"


#ifndef MY_CUSTOM_INTERFACES__MSG__DETAIL__POS_OBSTACLES__BUILDER_HPP_
#define MY_CUSTOM_INTERFACES__MSG__DETAIL__POS_OBSTACLES__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_custom_interfaces/msg/detail/pos_obstacles__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_custom_interfaces
{

namespace msg
{

namespace builder
{

class Init_PosObstacles_flotants
{
public:
  explicit Init_PosObstacles_flotants(::my_custom_interfaces::msg::PosObstacles & msg)
  : msg_(msg)
  {}
  ::my_custom_interfaces::msg::PosObstacles flotants(::my_custom_interfaces::msg::PosObstacles::_flotants_type arg)
  {
    msg_.flotants = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_custom_interfaces::msg::PosObstacles msg_;
};

class Init_PosObstacles_fixes
{
public:
  Init_PosObstacles_fixes()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PosObstacles_flotants fixes(::my_custom_interfaces::msg::PosObstacles::_fixes_type arg)
  {
    msg_.fixes = std::move(arg);
    return Init_PosObstacles_flotants(msg_);
  }

private:
  ::my_custom_interfaces::msg::PosObstacles msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_custom_interfaces::msg::PosObstacles>()
{
  return my_custom_interfaces::msg::builder::Init_PosObstacles_fixes();
}

}  // namespace my_custom_interfaces

#endif  // MY_CUSTOM_INTERFACES__MSG__DETAIL__POS_OBSTACLES__BUILDER_HPP_
