#!/bin/bash

# Function to check if user is in docker group
check_docker_group() {
    if ! groups | grep -q docker; then
        echo "Adding user to docker group..."
        sudo usermod -aG docker $USER
        echo "Please log out and log back in for the changes to take effect"
        exit 1
    fi
}

# Function to fix permissions
fix_permissions() {
    local project_dir="$1"
    echo "Fixing permissions for $project_dir..."
    
    # Fix ownership of project files
    sudo chown -R $USER:$USER "$project_dir"
    
    # Fix permissions for directories
    find "$project_dir" -type d -exec chmod 755 {} \;
    
    # Fix permissions for files
    find "$project_dir" -type f -exec chmod 644 {} \;
    
    # Make scripts executable
    find "$project_dir" -name "*.sh" -type f -exec chmod +x {} \;
}

# Function to manage containers
manage_containers() {
    local action="$1"
    local service="$2"
    local compose_file="wellness_solutions/docker-compose.local.yml"
    
    case "$action" in
        "start")
            docker-compose -f "$compose_file" up -d "$service"
            ;;
        "stop")
            docker-compose -f "$compose_file" stop "$service"
            ;;
        "restart")
            docker-compose -f "$compose_file" restart "$service"
            ;;
        "rebuild")
            docker-compose -f "$compose_file" build "$service"
            docker-compose -f "$compose_file" up -d --force-recreate "$service"
            ;;
        *)
            echo "Invalid action. Use: start, stop, restart, or rebuild"
            exit 1
            ;;
    esac
}

# Main script
main() {
    local command="$1"
    local service="$2"
    local project_dir="/home/meshack-vs-you-all/CascadeProjects/wellness_solutions"
    
    # Always check docker group
    check_docker_group
    
    case "$command" in
        "fix-perms")
            fix_permissions "$project_dir"
            ;;
        "start"|"stop"|"restart"|"rebuild")
            manage_containers "$command" "$service"
            ;;
        *)
            echo "Usage: $0 {fix-perms|start|stop|restart|rebuild} [service]"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
