// Copyright (c) 2024, Ragapp Technologies and contributors
// For license information, please see license.txt

ragapp.ui.form.on("Role Replication", {
	refresh(frm) {
		frm.disable_save();
		frm.page.set_primary_action(__("Replicate"), ($btn) => {
			$btn.text(__("Replicating..."));
			ragapp.run_serially([
				() => ragapp.dom.freeze("Replicating..."),
				() => frm.call("replicate_role"),
				() => ragapp.dom.unfreeze(),
				() => ragapp.msgprint(__("Replication completed.")),
				() => $btn.text(__("Replicate")),
			]);
		});
	},
});
