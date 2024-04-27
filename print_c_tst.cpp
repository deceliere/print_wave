#include </usr/local/opt/cups/include/cups/cups.h>

int main() {
    // Initialize CUPS
    cups_dest_t *dests;
    int num_dests = cupsGetDests(&dests);
    
    // Get default printer
    const char *printer_name = cupsGetDefault();
    
    // Print to default printer
    if (printer_name != nullptr) {
        cupsPrintFile(printer_name, "path_to_your_file", "YourDocument", num_options, options);
    } else {
        std::cerr << "No default printer found\n";
    }
    
    // Free resources
    cupsFreeDests(num_dests, dests);
    
    return 0;
}
