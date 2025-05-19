"""
Python Media Converter
Allows converting between various media formats with a user-friendly menu interface.
"""

import os
import sys
import glob
import ffmpeg
from typing import List, Dict, Tuple

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the program header."""
    print("=" * 60)
    print("               PYTHON MEDIA CONVERTER")
    print("                   Coded by: @s4rrar")
    print("=" * 60)
    print()

def convert_file(input_path: str, output_path: str) -> bool:
    """
    Convert a single file using ffmpeg.
    
    Args:
        input_path: Path to the input file
        output_path: Path to the output file
        
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Run the conversion
        ffmpeg.input(input_path).output(output_path, loglevel="error").run(overwrite_output=True)
        print(f"✓ Conversion successful: {output_path}")
        return True
    except ffmpeg.Error as e:
        print(f"✗ Error converting {input_path}: {e.stderr.decode() if hasattr(e, 'stderr') else str(e)}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error converting {input_path}: {str(e)}")
        return False

def get_media_files_in_directory(directory: str = '.') -> Dict[str, List[str]]:
    """
    Get all media files in the specified directory, grouped by extension.
    
    Args:
        directory: Directory to scan for media files
        
    Returns:
        Dict mapping file extensions to lists of file paths
    """
    # Common media file extensions
    media_extensions = [
        # Video formats
        "*.mp4", "*.avi", "*.mkv", "*.mov", "*.wmv", "*.flv", "*.webm", "*.m4v", "*.ts", "*.3gp",
        # Audio formats
        "*.mp3", "*.wav", "*.flac", "*.aac", "*.ogg", "*.wma", "*.m4a", "*.opus",
        # Image formats
        "*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff", "*.webp",
        # Other media formats
        "*.vob", "*.mpg", "*.mpeg", "*.mxf", "*.divx", "*.m2ts"
    ]
    
    files_by_extension = {}
    
    for pattern in media_extensions:
        files = glob.glob(os.path.join(directory, pattern))
        if files:
            ext = pattern[1:]  # Remove the '*' from the pattern
            files_by_extension[ext] = files
    
    return files_by_extension

def get_input_format_menu(files_by_extension: Dict[str, List[str]]) -> str:
    """
    Display menu for selecting input format.
    
    Args:
        files_by_extension: Dict mapping file extensions to lists of file paths
        
    Returns:
        Selected input format (extension without dot) or None to exit
    """
    clear_screen()
    print_header()
    print("Available input formats in current directory:")
    print()
    
    if not files_by_extension:
        print("No media files found in the current directory.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Sort extensions alphabetically
    sorted_extensions = sorted(files_by_extension.keys())
    
    for i, ext in enumerate(sorted_extensions, 1):
        count = len(files_by_extension[ext])
        print(f"{i}. {ext} ({count} file{'s' if count > 1 else ''})")
    
    print()
    print("0. Exit program")
    print()
    
    while True:
        try:
            choice = input("Select input format (number or 0 to exit): ")
            if choice.lower() in ('q', 'exit', 'quit'):
                return None
            
            choice = int(choice)
            if choice == 0:
                return None
            elif 1 <= choice <= len(sorted_extensions):
                return sorted_extensions[choice - 1]
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def get_output_format() -> str:
    """
    Get the desired output format from user.
    
    Returns:
        Output format (extension without dot) or None to cancel
    """
    clear_screen()
    print_header()
    print("Common output formats:")
    print()
    
    common_formats = [
        # Video formats
        "mp4", "avi", "mkv", "mov", "webm", "m4v", 
        # Audio formats
        "mp3", "wav", "flac", "aac", "ogg", "m4a",
        # Image formats
        "jpg", "png", "gif", "webp"
    ]
    
    # Display in columns
    columns = 4
    for i in range(0, len(common_formats), columns):
        row = common_formats[i:i+columns]
        print("  ".join(f"{i+j+1}. {fmt}" for j, fmt in enumerate(row)))
    
    print()
    print("C. Custom format (enter your own)")
    print("0. Cancel/Go back")
    print()
    
    while True:
        choice = input("Select output format (number, C for custom, or 0 to cancel): ").strip().upper()
        
        if choice in ('0', 'Q', 'CANCEL', 'BACK'):
            return None
        
        if choice == 'C':
            custom_format = input("Enter custom output format (without dot, or 0 to cancel): ").strip().lower()
            if custom_format == '0':
                return None
            if custom_format and not custom_format.startswith('.'):
                return custom_format
        else:
            try:
                choice_num = int(choice)
                if choice_num == 0:
                    return None
                if 1 <= choice_num <= len(common_formats):
                    return common_formats[choice_num - 1]
            except ValueError:
                pass
                
        print("Invalid choice. Please try again.")

def select_files_menu(input_format: str, files: List[str]) -> List[str]:
    """
    Menu for selecting which files to convert.
    
    Args:
        input_format: Input format extension
        files: List of files with the selected input format
        
    Returns:
        List of files to convert or empty list to cancel
    """
    clear_screen()
    print_header()
    print(f"Files with .{input_format} extension:")
    print()
    
    # Sort files alphabetically
    sorted_files = sorted(files)
    
    # Display files with numbers
    for i, file in enumerate(sorted_files, 1):
        print(f"{i}. {os.path.basename(file)}")
    
    print()
    print("-1. Convert ALL files")
    print(" 0. Cancel/Go back")
    print()
    
    while True:
        try:
            choice = input("Select file to convert (number, -1 for all, comma-separated list, or 0 to cancel): ")
            
            if choice.lower() in ('cancel', 'back', 'q', 'quit', 'exit'):
                return []
                
            # Check for multiple selections (comma-separated)
            if ',' in choice:
                indices = [int(x.strip()) for x in choice.split(',')]
                selected_files = []
                
                for idx in indices:
                    if idx == 0:
                        return []  # Cancel if 0 is in the list
                    elif 1 <= idx <= len(sorted_files):
                        selected_files.append(sorted_files[idx - 1])
                    else:
                        print(f"Invalid selection: {idx}")
                
                if selected_files:
                    return selected_files
                
            # Check for single selection
            else:
                choice = int(choice)
                
                if choice == -1:
                    return sorted_files
                elif choice == 0:
                    return []
                elif 1 <= choice <= len(sorted_files):
                    return [sorted_files[choice - 1]]
            
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number or comma-separated list.")

def convert_files(input_files: List[str], input_format: str, output_format: str) -> Tuple[int, int]:
    """
    Convert multiple files from one format to another.
    
    Args:
        input_files: List of input file paths
        input_format: Input format extension
        output_format: Output format extension
        
    Returns:
        Tuple of (successful conversions, failed conversions)
    """
    if not input_files:
        return 0, 0
    
    output_dir = input("Enter output directory (leave empty for current directory, or 'cancel' to abort): ").strip()
    
    if output_dir.lower() in ('cancel', 'exit', 'quit'):
        print("Conversion cancelled.")
        return 0, 0
    
    if output_dir and not os.path.exists(output_dir):
        create_dir = input(f"Directory '{output_dir}' doesn't exist. Create it? (y/n): ")
        if create_dir.lower() == 'y':
            try:
                os.makedirs(output_dir)
            except Exception as e:
                print(f"Error creating directory: {str(e)}")
                return 0, 0
        else:
            return 0, 0
    
    print(f"\nConverting {len(input_files)} file(s) from .{input_format} to .{output_format}...")
    print("Press Ctrl+C at any time to cancel the conversion process.\n")
    
    success_count = 0
    failed_count = 0
    
    try:
        for i, input_file in enumerate(input_files, 1):
            base_name = os.path.basename(input_file)
            name_without_ext = os.path.splitext(base_name)[0]
            output_file = os.path.join(output_dir if output_dir else '', f"{name_without_ext}.{output_format}")
            
            print(f"[{i}/{len(input_files)}] Converting: {base_name}")
            
            if convert_file(input_file, output_file):
                success_count += 1
            else:
                failed_count += 1
    except KeyboardInterrupt:
        print("\nConversion process cancelled by user.")
        
    return success_count, failed_count

def main_menu():
    """Main menu function."""
    while True:
        clear_screen()
        print_header()
        
        print("1. Convert media files")
        print("0. Exit program")
        print()
        
        choice = input("Select an option (0-1): ")
        
        if choice == '0' or choice.lower() in ('q', 'exit', 'quit'):
            print("\nExiting program. Goodbye!")
            sys.exit(0)
        elif choice != '1':
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")
            continue
            
        # Get media files in current directory
        files_by_extension = get_media_files_in_directory()
        
        # Select input format
        input_format = get_input_format_menu(files_by_extension)
        if input_format is None:
            continue
            
        input_files = files_by_extension[input_format]
        
        # Select output format
        output_format = get_output_format()
        if output_format is None:
            continue
        
        # Select files to convert
        files_to_convert = select_files_menu(input_format, input_files)
        
        if files_to_convert:
            # Perform conversion
            success, failed = convert_files(files_to_convert, input_format, output_format)
            
            print(f"\nConversion complete: {success} succeeded, {failed} failed.")
            input("\nPress Enter to continue...")
        else:
            print("No files selected for conversion.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting program. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)
