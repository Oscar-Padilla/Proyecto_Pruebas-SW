import { test, expect } from '@playwright/test';
import { TIMEOUT } from 'dns';

test('Test de inicio de sesión', async ({ page }) => {

  await page.goto('https://www.zegucom.com.mx/');

  await expect(page).toHaveTitle(/Inicio | Zegucom Cómputo/);

  const ButtonLogIn1 = page.locator("a[id='dd_acount_wos']");
  await expect(ButtonLogIn1).toBeVisible();
  await ButtonLogIn1.click();

  const ButtonLogIn2 = page.locator("a[href='/site/login']").nth(0);
  await expect(ButtonLogIn2).toBeVisible();
  await ButtonLogIn2.click();

  const AccountInput = page.locator("input[id='loginform-username']");
  await AccountInput.fill("pruebaspage264@gmail.com");

  const PasswordInput = page.locator("input[id='loginform-password'] ");
  await PasswordInput.fill("987456321Pruebas");

  await page.keyboard.press('Enter');
  await expect(page.locator("a[id='dd_btn_acount']")).toContainText("YahelPruebas",{ timeout: 0 });


});

test('Test de inicio de sesión con datos incorrectos', async ({page})=> {

  await page.goto('https://www.zegucom.com.mx/');

  await expect(page).toHaveTitle(/Inicio | Zegucom Cómputo/);

  const ButtonLogIn1 = page.locator("a[id='dd_acount_wos']");
  await expect(ButtonLogIn1).toBeVisible();
  await ButtonLogIn1.click();

  const ButtonLogIn2 = page.locator("a[href='/site/login']").nth(0);
  await expect(ButtonLogIn2).toBeVisible();
  await ButtonLogIn2.click();

  const AccountInput = page.locator("input[id='loginform-username']");
  await AccountInput.fill("XXXXXXXXXXXXXXXXXXXXXXXX");

  const PasswordInput = page.locator("input[id='loginform-password'] ");
  await PasswordInput.fill("987456321Pruebass");

  await page.keyboard.press('Enter');
  const errorMessage = page.locator("p[class='help-block help-block-error']").nth(1);
  await expect(errorMessage).toContainText("El usuario o la contraseña son incorrectos.");

});

test('Barra de busqueda', async ({page})=> {
  await page.goto('https://www.zegucom.com.mx/');
  await expect(page).toHaveTitle(/Inicio | Zegucom Cómputo/);

  const searchInput = page.locator("input[class='input-search-autocomplete search']");
  await expect(searchInput).toBeVisible();

  await searchInput.fill("laptops");
  await new Promise(resolve => setTimeout(resolve, 2000)); 
  await page.keyboard.press('Enter');

  const button = page.locator("button[dfd-value-term='laptops']").nth(0);
  await expect(button).toBeVisible();

  await expect(button).toContainText("laptops");

});

test('Producto carrito', async ({page})=> {
  await page.goto('https://www.zegucom.com.mx/');
  await expect(page).toHaveTitle(/Inicio | Zegucom Cómputo/);


  const ButtonItem1 = page.locator("div[class='row carousel-item active']").nth(0);
  await expect(ButtonItem1).toBeVisible();
  await ButtonItem1.click();

  const ButtonItem2 = page.locator("a[id='btn-car']").nth(1);
  await expect(ButtonItem2).toBeVisible();
  await new Promise(resolve => setTimeout(resolve, 2000)); 
  await ButtonItem2.click();

  const ButtonItem3 = page.locator("a[class='add-to-cart rounded btn amber grey-text text-darken-4 z-depth-0']");
  await expect(ButtonItem3).toBeVisible();
  await ButtonItem3.click();

  const ButtonItem4 = page.locator("a[href='/z-cart/index']");
  await expect(ButtonItem4).toBeVisible();
  await ButtonItem4.click();

  const button = page.locator("a[href='/z-cart/delivery-method']");
  await expect(button).toBeVisible();
  await expect(button).toContainText("Siguiente");

})

test('ir a pagar', async ({ page }) => {

  await page.goto('https://www.zegucom.com.mx/');

  await expect(page).toHaveTitle(/Inicio | Zegucom Cómputo/);

  const ButtonLogIn1 = page.locator("a[id='dd_acount_wos']");
  await expect(ButtonLogIn1).toBeVisible();
  await ButtonLogIn1.click();

  const ButtonLogIn2 = page.locator("a[href='/site/login']").nth(0);;
  await expect(ButtonLogIn2).toBeVisible();
  await ButtonLogIn2.click();

  const AccountInput = page.locator("input[id='loginform-username']");
  await AccountInput.fill("pruebaspage264@gmail.com");

  const PasswordInput = page.locator("input[id='loginform-password'] ");
  await PasswordInput.fill("987456321Pruebas");

  await page.keyboard.press('Enter');
  await expect(page.locator("a[id='dd_btn_acount']")).toContainText("YahelPruebas", { timeout: 0 });

  const searchInput = page.locator('input.input-search-autocomplete.search');
  await page.waitForSelector('input.input-search-autocomplete.search', { state: 'visible' });
  await expect(searchInput).toBeVisible();

  await searchInput.fill("laptops");
  await page.keyboard.press('Enter');

  const productButton = page.locator("a[class='black-text selectItem ']").nth(3);
  await expect(productButton).toBeVisible({ timeout: 0 });
  await productButton.click();

  const agregar = page.locator("i[class='material-icons mr-1']").nth(1);
  await expect(agregar).toBeVisible({ timeout: 0 });
  await agregar.click();

  try {
    // Espera a que la ventana sea visible (máximo 10 segundos)
    await page.waitForSelector("div[aria-labelledby='swal2-title']", { timeout: 10000 });

    // Una vez visible, continúa con las acciones
    const botonconfirmar = page.locator("button[class='swal2-confirm swal2-styled']");
    await expect(botonconfirmar).toBeVisible(); // Verifica que el botón está visible
    await botonconfirmar.click(); // Haz clic en el botón
  } catch (e) {
    console.log("La ventana no apareció dentro del tiempo esperado.");
  }

  const carritobtn = page.locator("a[href='/z-cart/index']");
  await expect(carritobtn).toBeVisible();
  await carritobtn.click();

  // const agregar2 = page.locator("a[href='/z-cart/index']");
  // await expect(agregar2).toBeVisible();
  // await agregar2.click();

  const deliverybtn = page.locator("a[href='/z-cart/delivery-method']");
  await expect(deliverybtn).toBeVisible();
  await deliverybtn.click();

  const pgrbtn = page.locator('a:has-text("Siguiente")');
  await expect(pgrbtn).toBeVisible();
  await pgrbtn.click();

  const metpag = page.locator('span:has-text("Tarjeta de Débito/Crédito (todas las tarjetas)")');
  await expect(metpag).toBeVisible({ timeout: 0 });
  await metpag.click();
  await new Promise(resolve => setTimeout(resolve, 5000));

  const pagarbtn = page.locator('button:has-text("Pagar")');
  await expect(pagarbtn).toBeVisible({ timeout: 0 });

});

test('borrar carrito', async ({ page }) => {
  await page.goto('https://www.zegucom.com.mx/');

  await expect(page).toHaveTitle(/Inicio | Zegucom Cómputo/);

  const searchInput = page.locator('input.input-search-autocomplete.search');
  await page.waitForSelector('input.input-search-autocomplete.search', { state: 'visible' });
  await expect(searchInput).toBeVisible({ timeout: 0 });

  await searchInput.fill("laptops");
  await page.keyboard.press('Enter');

  const productButton = page.locator('img[src="/images/brands/webp/LV.webp"]').nth(0); // O el índice correcto
  await expect(productButton).toBeVisible({ timeout: 0 });
  await productButton.click();

  await page.waitForSelector('#btn-car', { state: 'visible' });
  await new Promise(resolve => setTimeout(resolve, 2000));
  await page.click('#btn-car');

  try {
    // Espera a que la ventana sea visible (máximo 10 segundos)
    await page.waitForSelector("div[aria-labelledby='swal2-title']", { timeout: 10000 });

    // Una vez visible, continúa con las acciones
    const botonconfirmar = page.locator("button[class='swal2-confirm swal2-styled']");
    await expect(botonconfirmar).toBeVisible(); // Verifica que el botón está visible
    await botonconfirmar.click(); // Haz clic en el botón
  } catch (e) {
    console.log("La ventana no apareció dentro del tiempo esperado.");
  }

  const carritobtn = page.locator("a[href='/z-cart/index']").nth(0);;
  await expect(carritobtn).toBeVisible({ timeout: 0 });
  await carritobtn.click();

  const deleteButton = page.locator('a:has-text("delete")');
  await expect(deleteButton).toBeVisible({ timeout: 0 });
  await deleteButton.click();

  const chiacepto = page.locator('button:has-text("Aceptar")');
  await expect(chiacepto).toBeVisible({ timeout: 0 });
  await chiacepto.click();

});