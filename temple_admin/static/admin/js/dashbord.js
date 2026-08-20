// ============================================================
// GET TOKEN
// ============================================================

const token = localStorage.getItem("access_token");


// ============================================================
// GET HTML ELEMENTS
// ============================================================

// Announcement
const announcementForm =
    document.getElementById("announcementForm");

const announcementTitle =
    document.getElementById("announcementTitle");

const announcementContent =
    document.getElementById("announcementContent");

const announcementMessage =
    document.getElementById("announcementMessage");


// Gallery
const galleryUploadForm =
    document.getElementById("galleryUploadForm");

const galleryImage =
    document.getElementById("galleryImage");

const galleryCaption =
    document.getElementById("galleryCaption");

const galleryMessage =
    document.getElementById("galleryMessage");

const galleryContainer =
    document.getElementById("galleryContainer");


// Logout
const logoutBtn =
    document.getElementById("logoutBtn");


// ============================================================
// CHECK TOKEN
// ============================================================

if (!token) {
    window.location.href = "/admin/login";
}


// ============================================================
// LOAD ANNOUNCEMENT
// ============================================================

let announcementId = null;


async function loadAnnouncement() {

    try {

        const response = await fetch("/api/announcement");

        const data = await response.json();

        console.log("Announcement:", data);


        if (!response.ok) {

            announcementMessage.textContent =
                data.error || "Failed to load announcement";

            return;
        }


        // Save the UUID because PATCH needs it
        announcementId = data.id;


        // Put database values into HTML
        announcementTitle.value = data.title;
        announcementContent.value = data.content;


    } catch (error) {

        console.error("Announcement error:", error);

        announcementMessage.textContent =
            "Failed to load announcement.";
    }
}


// ============================================================
// UPDATE ANNOUNCEMENT
// ============================================================

announcementForm.addEventListener("submit", async (event) => {

    event.preventDefault();


    const title = announcementTitle.value;
    const content = announcementContent.value;


    try {

        const response = await fetch(
            "/api/admin/announcement",
            {
                method: "PATCH",

                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    id: announcementId,
                    title: title,
                    content: content
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            announcementMessage.textContent =
                data.error || "Failed to update announcement";

            return;
        }


        announcementMessage.textContent =
            "Announcement updated successfully.";


        console.log("Updated announcement:", data);


    } catch (error) {

        console.error("Update error:", error);

        announcementMessage.textContent =
            "Something went wrong.";
    }

});


// ============================================================
// LOAD GALLERY
// ============================================================

async function loadGallery() {

    try {

        const response =
            await fetch("/api/gallery");

        const data =
            await response.json();


        console.log("Gallery:", data);


        if (!response.ok) {

            galleryContainer.textContent =
                data.error || "Failed to load gallery";

            return;
        }


        // Remove old content
        galleryContainer.innerHTML = "";


        // No images
        if (data.length === 0) {

            galleryContainer.textContent =
                "No gallery images found.";

            return;
        }


        // Create HTML for every image
        data.forEach((item) => {

            const galleryItem =
                document.createElement("div");


            const image =
                document.createElement("img");

            image.src = item.image_url;
            image.alt = item.caption || "Gallery image";

            image.width = 200;


            const caption =
                document.createElement("p");

            caption.textContent =
                item.caption || "";


            const deleteButton =
                document.createElement("button");

            deleteButton.textContent =
                "Delete";


            // Store UUID on the button
            deleteButton.dataset.id =
                item.id;


            // Delete when clicked
            deleteButton.addEventListener(
                "click",
                () => deleteGalleryImage(item.id)
            );


            galleryItem.appendChild(image);
            galleryItem.appendChild(caption);
            galleryItem.appendChild(deleteButton);


            galleryContainer.appendChild(galleryItem);

        });


    } catch (error) {

        console.error("Gallery error:", error);

        galleryContainer.textContent =
            "Failed to load gallery.";
    }
}


// ============================================================
// UPLOAD GALLERY IMAGE
// ============================================================

galleryUploadForm.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();


        const file =
            galleryImage.files[0];

        const caption =
            galleryCaption.value;


        if (!file) {

            galleryMessage.textContent =
                "Please select an image.";

            return;
        }


        // FormData is used for file uploads
        const formData =
            new FormData();


        formData.append(
            "image",
            file
        );

        formData.append(
            "caption",
            caption
        );


        try {

            const response = await fetch(
                "/api/admin/gallery",
                {
                    method: "POST",

                    headers: {
                        "Authorization": `Bearer ${token}`
                    },

                    body: formData
                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                galleryMessage.textContent =
                    data.error || "Upload failed";

                return;
            }


            galleryMessage.textContent =
                "Image uploaded successfully.";


            // Clear form
            galleryUploadForm.reset();


            // Reload gallery
            loadGallery();


        } catch (error) {

            console.error("Upload error:", error);

            galleryMessage.textContent =
                "Something went wrong.";
        }

    }
);


// ============================================================
// DELETE GALLERY IMAGE
// ============================================================

async function deleteGalleryImage(id) {

    const confirmed =
        confirm("Are you sure you want to delete this image?");


    if (!confirmed) {
        return;
    }


    try {

        const response = await fetch(
            `/api/admin/gallery/${id}`,
            {
                method: "DELETE",

                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );


        const data =
            await response.json();


        if (!response.ok) {

            galleryMessage.textContent =
                data.error || "Delete failed";

            return;
        }


        galleryMessage.textContent =
            "Image deleted successfully.";


        // Reload gallery after deletion
        loadGallery();


    } catch (error) {

        console.error("Delete error:", error);

        galleryMessage.textContent =
            "Something went wrong.";
    }
}


// ============================================================
// LOGOUT
// ============================================================

logoutBtn.addEventListener(
    "click",
    async () => {

        try {

            const response = await fetch(
                "/api/auth/logout",
                {
                    method: "POST",

                    headers: {
                        "Authorization": `Bearer ${token}`
                    }
                }
            );


            if (response.ok) {

                // Remove token from browser
                localStorage.removeItem(
                    "access_token"
                );

                // Send user back to login
                window.location.href =
                    "/admin/login";

                return;
            }


            console.error(
                "Logout failed"
            );


        } catch (error) {

            console.error(
                "Logout error:",
                error
            );
        }

    }
);


// ============================================================
// START DASHBOARD
// ============================================================

loadAnnouncement();

loadGallery();